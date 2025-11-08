import asyncio
import time
import json
import uuid
import os
import websockets
import gzip
import random
from urllib import parse
from tabulate import tabulate
from config.settings import load_config
import tempfile
import wave
import hmac
import base64
import hashlib
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
description = "Streaming ASR first word delay test"
try:
    import dashscope
except ImportError:
    dashscope = None

class BaseASRTester:
    def __init__(self, config_key: str):
        self.config = load_config()
        self.config_key = config_key
        self.asr_config = self.config.get("ASR", {}).get(config_key, {})
        self.test_audio_files = self._load_test_audio_files()
        self.results = []

    def _load_test_audio_files(self):
        audio_root = os.path.join(os.getcwd(), "config", "assets")
        test_files = []
        if os.path.exists(audio_root):
            for file_name in os.listdir(audio_root):
                if file_name.endswith(('.wav', '.pcm')):
                    file_path = os.path.join(audio_root, file_name)
                    with open(file_path, 'rb') as f:
                        test_files.append({
                            'data': f.read(),
                            'path': file_path,
                            'name': file_name
                        })
        return test_files

    async def test(self, test_count=5):
        raise NotImplementedError

    def _calculate_result(self, service_name, latencies, test_count):
        valid_latencies = [l for l in latencies if l > 0]
        if valid_latencies:
            avg_latency = sum(valid_latencies) / len(valid_latencies)
            status = f"Success ({len(valid_latencies)}/{test_count} times valid)"
        else:
            avg_latency = 0
            status = "FAILED: All tests failed"
        return {"name": service_name, "latency": avg_latency, "status": status}


class DoubaoStreamASRTester(BaseASRTester):
    def __init__(self):
        super().__init__("DoubaoStreamASR")

    def _generate_header(self):
        header = bytearray()
        header.append((0x01 << 4) | 0x01)
        header.append((0x01 << 4) | 0x00)
        header.append((0x01 << 4) | 0x01)
        header.append(0x00)
        return header

    def _generate_audio_default_header(self):
        return self._generate_header()

    def _parse_response(self, res: bytes) -> dict:
        try:
            if len(res) < 4:
                return {"error": "Insufficient response data length"}
            header = res[:4]
            message_type = header[1] >> 4
            if message_type == 0x0F:
                code = int.from_bytes(res[4:8], "big", signed=False)
                msg_length = int.from_bytes(res[8:12], "big", signed=False)
                error_msg = json.loads(res[12:].decode("utf-8"))
                return {
                    "code": code,
                    "msg_length": msg_length,
                    "payload_msg": error_msg
                }
            try:
                json_data = res[12:].decode("utf-8")
                return {"payload_msg": json.loads(json_data)}
            except (UnicodeDecodeError, json.JSONDecodeError):
                return {"error": "JSON parsing failed"}
        except Exception:
            return {"error": "Failed to parse response"}

    async def test(self, test_count=5):
        if not self.test_audio_files:
            return {"name": "Bean bag streaming ASR", "latency": 0, "status": "Failure: Test audio not found"}
        if not self.asr_config:
            return {"name": "Bean bag streaming ASR", "latency": 0, "status": "Failure: Not configured"}

        latencies = []
        for i in range(test_count):
            try:
                ws_url = "wss://openspeech.bytedance.com/api/v3/sauc/bigmodel"
                appid = self.asr_config["appid"]
                access_token = self.asr_config["access_token"]
                uid = self.asr_config.get("uid", "streaming_asr_service")

                start_time = time.time()

                headers = {
                    "X-Api-App-Key": appid,
                    "X-Api-Access-Key": access_token,
                    "X-Api-Resource-Id": "volc.bigasr.sauc.duration",
                    "X-Api-Connect-Id": str(uuid.uuid4())
                }

                async with websockets.connect(
                    ws_url,
                    additional_headers=headers,
                    max_size=1000000000,
                    ping_interval=None,
                    ping_timeout=None,
                    close_timeout=10
                ) as ws:
                    request_params = {
                        "app": {"appid": appid, "token": access_token},
                        "user": {"uid": uid},
                        "request": {
                            "reqid": str(uuid.uuid4()),
                            "workflow": "audio_in,resample,partition,vad,fe,decode,itn,nlu_punctuate",
                            "show_utterances": True,
                            "result_type": "single",
                            "sequence": 1
                        },
                        "audio": {
                            "format": "pcm",
                            "codec": "pcm",
                            "rate": 16000,
                            "language": "zh-CN",
                            "bits": 16,
                            "channel": 1,
                            "sample_rate": 16000
                        }
                    }

                    payload_bytes = str.encode(json.dumps(request_params))
                    payload_bytes = gzip.compress(payload_bytes)
                    full_client_request = self._generate_header()
                    full_client_request.extend((len(payload_bytes)).to_bytes(4, "big"))
                    full_client_request.extend(payload_bytes)
                    await ws.send(full_client_request)

                    init_res = await ws.recv()
                    result = self._parse_response(init_res)
                    if "code" in result and result["code"] != 1000:
                        raise Exception(f"Initialization failed: {result.get('payload_msg', {}).get('error', 'Unknown error')}")

                    audio_data = self.test_audio_files[0]['data']
                    if audio_data.startswith(b'RIFF'):
                        audio_data = audio_data[44:]

                    payload = gzip.compress(audio_data)
                    audio_request = bytearray(self._generate_audio_default_header())
                    audio_request.extend(len(payload).to_bytes(4, "big"))
                    audio_request.extend(payload)
                    await ws.send(audio_request)

                    first_chunk = await ws.recv()
                    latency = time.time() - start_time
                    latencies.append(latency)
                    await ws.close()

            except Exception as e:
                print(f"[豆包ASR] The {i+1}th test failed: {str(e)}")
                latencies.append(0)

        return self._calculate_result("Bean bag streaming ASR", latencies, test_count)


class QwenASRFlashTester(BaseASRTester):
    def __init__(self):
        super().__init__("Qwen3ASRFlash")

    async def _test_single(self, audio_file_info):
        start_time = time.time()
        temp_file_path = None

        try:
            audio_data = audio_file_info['data']
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                temp_file_path = f.name

            with wave.open(temp_file_path, 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(16000)
                wav_file.writeframes(audio_data)

            messages = [
                {
                    "role": "user",
                    "content": [
                        {"audio": temp_file_path}
                    ]
                }
            ]

            api_key = self.asr_config.get("api_key") or os.getenv("DASHSCOPE_API_KEY")
            if not api_key:
                raise ValueError("api_key not configured")

            if dashscope is None:
                raise RuntimeError("dashscope library not installed")

            dashscope.api_key = api_key

            response = dashscope.MultiModalConversation.call(
                model="qwen3-asr-flash",
                messages=messages,
                result_format="message",
                asr_options={"enable_lid": True, "enable_itn": False},
                stream=True
            )

            for chunk in response:
                latency = time.time() - start_time
                return latency

            raise Exception("Streaming ended, no response received")

        except Exception as e:
            raise Exception(f"General ASR streaming failure: {str(e)}")

        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except:
                    pass

    async def test(self, test_count=5):
        if not self.test_audio_files:
            return {"name": "Tongyi Qianwen ASR", "latency": 0, "status": "Failure: Test audio not found"}
        if not self.asr_config and not os.getenv("DASHSCOPE_API_KEY"):
            return {"name": "Tongyi Qianwen ASR", "latency": 0, "status": "Failure: api_key not configured"}

        latencies = []
        for i in range(test_count):
            try:
                # print(f"\n[General ASR] starts the {i+1}th test...")+1}th test...")
                latency = await self._test_single(self.test_audio_files[0])
                latencies.append(latency)
                # print(f"[General meaning ASR] {i+1}th success delay: {latency:.3f}s") {latency:.3f}s")
            except Exception as e:
                # print(f"[General ASR] The {i+1}th test failed: {str(e)}")failed: {str(e)}")
                latencies.append(0)

        return self._calculate_result("Tongyi Qianwen ASR", latencies, test_count)


class XunfeiStreamASRTester(BaseASRTester):
    def __init__(self):
        super().__init__("XunfeiStreamASR")
        
    def _create_url(self):
        """Generate iFlytek ASR certification URL"""
        url = 'ws://iat.cn-huabei-1.xf-yun.com/v1'
        # Generate timestamp in RFC1123 format
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # Concatenate strings
        signature_origin = "host: " + "iat.cn-huabei-1.xf-yun.com" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v1 " + "HTTP/1.1"

        # Encrypt with hmac-sha256
        signature_sha = hmac.new(self.asr_config["api_secret"].encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.asr_config["api_key"], "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # Combine the requested authentication parameters into a dictionary
        v = {
            "authorization": authorization,
            "date": date,
            "host": "iat.cn-huabei-1.xf-yun.com"
        }

        # Splice authentication parameters to generate url
        url = url + '?' + parse.urlencode(v)
        return url
    
    async def test(self, test_count=5):
        if not self.test_audio_files:
            return {"name": "iFlytek streaming ASR", "latency": 0, "status": "Failure: Test audio not found"}
        if not self.asr_config:
            return {"name": "iFlytek streaming ASR", "latency": 0, "status": "Failure: Not configured"}
        
        # Check necessary configuration parameters
        required_keys = ["app_id", "api_key", "api_secret"]
        for key in required_keys:
            if key not in self.asr_config:
                return {"name": "iFlytek streaming ASR", "latency": 0, "status": f"Failure: Missing configuration item {key}"}
    
        latencies = []
        STATUS_FIRST_FRAME = 0
        
        for i in range(test_count):
            try:
                # Generate authentication URL
                ws_url = self._create_url()
                
                # Get audio data
                audio_data = self.test_audio_files[0]['data']
                if audio_data.startswith(b'RIFF'):
                    audio_data = audio_data[44:]  # Skip WAV file header
                
                # Identification parameters
                iat_params = {
                    "domain": self.asr_config.get("domain", "slm"),
                    "language": self.asr_config.get("language", "zh_cn"),
                    "accent": self.asr_config.get("accent", "mandarin"),
                    "dwa": self.asr_config.get("dwa", "wpgs"),
                    "result": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "plain"
                    }
                }
                
                # Prepare first frame data
                first_frame_data = {
                    "header": {
                        "status": STATUS_FIRST_FRAME,
                        "app_id": self.asr_config["app_id"]
                    },
                    "parameter": {
                        "iat": iat_params
                    },
                    "payload": {
                        "audio": {
                            "audio": base64.b64encode(audio_data[:960]).decode('utf-8'),
                            "sample_rate": 16000,
                            "encoding": "raw"
                        }
                    }
                }
                
                # Start the connection and measure the time
                start_time = time.time()
                
                async with websockets.connect(
                    ws_url,
                    max_size=1000000000,
                    ping_interval=None,
                    ping_timeout=None,
                    close_timeout=30,
                ) as ws:
                    # Send first frame data
                    await ws.send(json.dumps(first_frame_data, ensure_ascii=False))
                    print(f"[iFlytek ASR] Test {i+1}: The first frame has been sent, waiting for response...")
                    
                    # Directly wait for the first response and calculate the delay
                    # Refer to the implementation methods of Doubao and Tongyi Qianwen to simplify the logic
                    response_received = False
                    while not response_received:
                        try:
                            # Set a larger timeout
                            response = await asyncio.wait_for(ws.recv(), timeout=30.0)
                            
                            # 收到响应立即计算延迟，不管内容是什么
                            # This allows for accurate measurement of the arrival time of the first packet
                            latency = time.time() - start_time
                            latencies.append(latency)
                            response_received = True
                            
                            print(f"[iFlytek ASR] Test {i+1}: Received first packet response, delay: {latency:.3f}s")
                            break
                        except asyncio.TimeoutError:
                            print(f"[iFlytek ASR] {i+1} test: response timeout")
                            raise Exception("Get response timeout")
            except Exception as e:
                print(f"[iFlytek ASR] The {i+1}th test failed: {str(e)}")
                latencies.append(0)
        
        return self._calculate_result("iFlytek streaming ASR", latencies, test_count)

class ASRPerformanceSuite:
    def __init__(self):
        self.testers = []
        self.results = []

    def register_tester(self, tester_class):
        try:
            tester = tester_class()
            self.testers.append(tester)
            print(f"Registered tester: {tester.config_key}")
        except Exception as e:
            name_map = {
                "DoubaoStreamASRTester": "Bean bag streaming ASR",
                "QwenASRFlashTester": "Tongyi Qianwen ASR",
                "XunfeiStreamASRTester": "iFlytek streaming ASR"
            }
            name = name_map.get(tester_class.__name__, tester_class.__name__)
            print(f"Skip {name}: {str(e)}")

    def _print_results(self, test_count):
        if not self.results:
            print("No valid ASR test results")
            return

        print(f"\n{'='*60}")
        print("Streaming ASR first word response time test results")
        print(f"{'='*60}")
        print(f"Number of tests: Each ASR service is tested {test_count} times")

        success_results = sorted(
            [r for r in self.results if "success" in r["status"]],
            key=lambda x: x["latency"]
        )
        failed_results = [r for r in self.results if "success" not in r["status"]]

        table_data = [
            [r["name"], f"{r['latency']:.3f}s" if r['latency'] > 0 else "N/A", r["status"]]
            for r in success_results + failed_results
        ]

        print(tabulate(table_data, headers=["ASR service", "first word delay", "state"], tablefmt="grid"))
        print("\nTest description:")
        print("- Measure the time from sending a request to receiving the first valid recognized text")
        print("- Timeout control: DashScope defaults to timeout, Doubao WebSocket times out to 10 seconds")
        print("- Sorting rules: Successful ones are sorted in ascending order by delay, and failed ones are sorted later.")

    async def run(self, test_count=5):
        print(f"Start streaming ASR first word response time test...")
        print(f"Number of tests for each ASR service: {test_count} times\n")

        self.results = []
        for tester in self.testers:
            print(f"\n--- test {tester.config_key} ---")
            result = await tester.test(test_count)
            self.results.append(result)

        self._print_results(test_count)


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="Streaming ASR first word response time testing tool")
    parser.add_argument("--count", type=int, default=5, help="Number of tests")
    args = parser.parse_args()

    suite = ASRPerformanceSuite()
    suite.register_tester(DoubaoStreamASRTester)
    suite.register_tester(QwenASRFlashTester)
    suite.register_tester(XunfeiStreamASRTester)

    await suite.run(args.count)


if __name__ == "__main__":
    asyncio.run(main())