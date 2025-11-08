import json
import hmac
import base64
import hashlib
import asyncio
import websockets
import opuslib_next
from time import mktime
from datetime import datetime
from urllib.parse import urlencode
from typing import List
from config.logger import setup_logging
from wsgiref.handlers import format_date_time
from core.providers.asr.base import ASRProviderBase
from core.providers.asr.dto.dto import InterfaceType

TAG = __name__
logger = setup_logging()

# Frame status constant
STATUS_FIRST_FRAME = 0  # First frame identifier
STATUS_CONTINUE_FRAME = 1  # Intermediate frame identifier
STATUS_LAST_FRAME = 2  # The identifier of the last frame


class ASRProvider(ASRProviderBase):
    def __init__(self, config, delete_audio_file):
        super().__init__()
        self.interface_type = InterfaceType.STREAM
        self.config = config
        self.text = ""
        self.decoder = opuslib_next.Decoder(16000, 1)
        self.asr_ws = None
        self.forward_task = None
        self.is_processing = False
        self.server_ready = False
        self.last_frame_sent = False  # Flag whether the final frame has been sent
        self.best_text = ""  # Save the best recognition results
        self.has_final_result = False  # Whether the tag receives the final recognition result

        # iFlytek configuration
        self.app_id = config.get("app_id")
        self.api_key = config.get("api_key")
        self.api_secret = config.get("api_secret")

        if not all([self.app_id, self.api_key, self.api_secret]):
            raise ValueError("App_id, api_key and api_secret must be provided")

        # Identification parameters
        self.iat_params = {
            "domain": config.get("domain", "slm"),
            "language": config.get("language", "zh_cn"),
            "accent": config.get("accent", "mandarin"),
            "dwa": config.get("dwa", "wpgs"),
            "result": {"encoding": "utf8", "compress": "raw", "format": "plain"},
        }

        self.output_dir = config.get("output_dir", "tmp/")
        self.delete_audio_file = delete_audio_file

    def create_url(self) -> str:
        """Generate authentication URL"""
        url = "ws://iat.cn-huabei-1.xf-yun.com/v1"
        # Generate timestamp in RFC1123 format
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # Concatenate strings
        signature_origin = "host: " + "iat.cn-huabei-1.xf-yun.com" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v1 " + "HTTP/1.1"

        # Encrypt with hmac-sha256
        signature_sha = hmac.new(
            self.api_secret.encode("utf-8"),
            signature_origin.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding="utf-8")

        authorization_origin = (
            'api_key="%s", algorithm="%s", headers="%s", signature="%s"'
            % (self.api_key, "hmac-sha256", "host date request-line", signature_sha)
        )
        authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode(
            encoding="utf-8"
        )

        # Combine the requested authentication parameters into a dictionary
        v = {
            "authorization": authorization,
            "date": date,
            "host": "iat.cn-huabei-1.xf-yun.com",
        }

        # Splice authentication parameters to generate url
        url = url + "?" + urlencode(v)
        return url

    async def open_audio_channels(self, conn):
        await super().open_audio_channels(conn)

    async def receive_audio(self, conn, audio, audio_have_voice):
        # First call the parent class method to handle the basic logic
        await super().receive_audio(conn, audio, audio_have_voice)

        # Storing audio data for voiceprint recognition
        if not hasattr(conn, "asr_audio_for_voiceprint"):
            conn.asr_audio_for_voiceprint = []
        conn.asr_audio_for_voiceprint.append(audio)

        # If there is sound this time and no connection has been established before
        if audio_have_voice and self.asr_ws is None and not self.is_processing:
            try:
                await self._start_recognition(conn)
            except Exception as e:
                logger.bind(tag=TAG).error(f"Failed to establish ASR connection: {str(e)}")
                await self._cleanup(conn)
                return

        # Send current audio data
        if self.asr_ws and self.is_processing and self.server_ready:
            try:
                pcm_frame = self.decoder.decode(audio, 960)
                await self._send_audio_frame(pcm_frame, STATUS_CONTINUE_FRAME)
            except Exception as e:
                logger.bind(tag=TAG).warning(f"An error occurred while sending audio data: {e}")
                await self._cleanup(conn)

    async def _start_recognition(self, conn):
        """Start recognition session"""
        try:
            self.is_processing = True
            # Establish a WebSocket connection
            ws_url = self.create_url()
            logger.bind(tag=TAG).info(f"Connecting to ASR service: {ws_url[:50]}...")

            self.asr_ws = await websockets.connect(
                ws_url,
                max_size=1000000000,
                ping_interval=None,
                ping_timeout=None,
                close_timeout=10,
            )

            logger.bind(tag=TAG).info("ASR WebSocket connection established")
            self.server_ready = False
            self.last_frame_sent = False
            self.best_text = ""
            self.forward_task = asyncio.create_task(self._forward_results(conn))

            # Send the first frame of audio
            if conn.asr_audio and len(conn.asr_audio) > 0:
                first_audio = conn.asr_audio[-1] if conn.asr_audio else b""
                pcm_frame = (
                    self.decoder.decode(first_audio, 960) if first_audio else b""
                )
                await self._send_audio_frame(pcm_frame, STATUS_FIRST_FRAME)
                self.server_ready = True
                logger.bind(tag=TAG).info("The first frame has been sent and recognition started")

                # Send buffered audio data
                for cached_audio in conn.asr_audio[-10:]:
                    try:
                        pcm_frame = self.decoder.decode(cached_audio, 960)
                        await self._send_audio_frame(pcm_frame, STATUS_CONTINUE_FRAME)
                    except Exception as e:
                        logger.bind(tag=TAG).info(f"An error occurred while sending cached audio data: {e}")
                        break

        except Exception as e:
            logger.bind(tag=TAG).error(f"Failed to establish ASR connection: {str(e)}")
            if hasattr(e, "__cause__") and e.__cause__:
                logger.bind(tag=TAG).error(f"Error reason: {str(e.__cause__)}")
            if self.asr_ws:
                await self.asr_ws.close()
                self.asr_ws = None
            self.is_processing = False
            raise

    async def _send_audio_frame(self, audio_data: bytes, status: int):
        """Send audio frames"""
        if not self.asr_ws:
            return

        audio_b64 = base64.b64encode(audio_data).decode("utf-8")

        frame_data = {
            "header": {"status": status, "app_id": self.app_id},
            "parameter": {"iat": self.iat_params},
            "payload": {
                "audio": {"audio": audio_b64, "sample_rate": 16000, "encoding": "raw"}
            },
        }

        await self.asr_ws.send(json.dumps(frame_data, ensure_ascii=False))

        # Flag whether the final frame was sent
        if status == STATUS_LAST_FRAME:
            self.last_frame_sent = True
            logger.bind(tag=TAG).info("Mark final frame sent")

    async def _forward_results(self, conn):
        """Forward recognition results"""
        try:
            while self.asr_ws and not conn.stop_event.is_set():
                # Get the audio data of the current connection
                audio_data = getattr(conn, "asr_audio_for_voiceprint", [])
                try:
                    # If the final frame has been sent, increase the timeout to wait for the complete result
                    timeout = 3.0 if self.last_frame_sent else 30.0
                    response = await asyncio.wait_for(
                        self.asr_ws.recv(), timeout=timeout
                    )
                    result = json.loads(response)
                    logger.bind(tag=TAG).debug(f"Received ASR result: {result}")

                    header = result.get("header", {})
                    payload = result.get("payload", {})
                    code = header.get("code", 0)
                    status = header.get("status", 0)

                    if code != 0:
                        logger.bind(tag=TAG).error(
                            f"Recognition error, error code: {code}, message: {header.get('message', '')}"
                        )
                        if code in [10114, 10160]:  # connection problem
                            break
                        continue

                    # Process recognition results
                    if payload and "result" in payload:
                        text_data = payload["result"]["text"]
                        if text_data:
                            # Decode base64 text
                            decoded_text = base64.b64decode(text_data).decode("utf-8")
                            text_json = json.loads(decoded_text)

                            # Extract text content
                            text_ws = text_json.get("ws", [])
                            result_text = ""
                            for i in text_ws:
                                for j in i.get("cw", []):
                                    w = j.get("w", "")
                                    result_text += w

                            # Update recognition text - real-time update strategy
                            # Only checks if it is an empty string and no longer filters any punctuation characters
                            # This ensures that all recognized content, including punctuation, is updated in real time
                            if result_text and result_text.strip():
                                # Real-time update: updates under normal circumstances to improve response speed
                                should_update = True

                                # Save the best text
                                # 1. If the result is received after the recognition completion status or the final frame, save it first.
                                # 2. Otherwise save the longest meaningful text
                                # Cancel the filtering of punctuation marks and only check whether it is empty
                                # This preserves all recognized content, including various punctuation marks
                                is_valid_text = len(result_text.strip()) > 0

                                if (
                                    self.last_frame_sent or status == 2
                                ) and is_valid_text:
                                    self.best_text = result_text
                                    self.has_final_result = True  # Mark final result received
                                    logger.bind(tag=TAG).debug(
                                        f"Save the final recognition result: {self.best_text}"
                                    )
                                elif (
                                    len(result_text) > len(self.best_text)
                                    and is_valid_text
                                    and not self.has_final_result
                                ):
                                    self.best_text = result_text
                                    logger.bind(tag=TAG).debug(
                                        f"Save the best middle text: {self.best_text}"
                                    )

                                # If the final frame has been sent, only empty text is filtered
                                if self.last_frame_sent:
                                    # Only reject completely empty results
                                    if not result_text.strip():
                                        should_update = False
                                        logger.bind(tag=TAG).warning(
                                            f"Reject empty text after final frame"
                                        )

                                if should_update:
                                    # Process streaming recognition results to avoid content loss caused by simple replacement
                                    # 1. If it is an intermediate state (not after the final frame), it may need to be replaced with a more complete recognition
                                    # 2. If the result is received after the final frame, it may be a supplement to the previous text.
                                    if self.last_frame_sent:
                                        # Results received after the final frame may be supplementary content such as punctuation
                                        # Check if text needs to be merged instead of replaced
                                        # If the current text is pure punctuation and there is content before it, it should be appended rather than replaced.
                                        if len(
                                            self.text
                                        ) > 0 and result_text.strip() in [
                                            "。",
                                            ".",
                                            "?",
                                            "？",
                                            "!",
                                            "！",
                                            ",",
                                            "，",
                                            ";",
                                            "；",
                                        ]:
                                            # For punctuation, append to existing text
                                            self.text = (
                                                self.text.rstrip().rstrip("。.")
                                                + result_text
                                            )
                                        else:
                                            # In other cases, keep the replacement logic
                                            self.text = result_text
                                    else:
                                        # The intermediate state is replaced by the new recognition result
                                        self.text = result_text

                                    logger.bind(tag=TAG).info(
                                        f"Real-time update recognition text: {self.text} (last frame sent: {self.last_frame_sent})"
                                    )

                    # Recognition is completed, but if the final frame has not been sent yet, continue to wait.
                    if status == 2:
                        logger.bind(tag=TAG).info(
                            f"Recognition completion status has been reached, current recognition text: {self.text}"
                        )

                        # If the final frame has not been sent yet, continue to wait.
                        if not self.last_frame_sent:
                            logger.bind(tag=TAG).info(
                                "Recognition is completed but the final frame is not sent, continue to wait..."
                            )
                            continue

                        # Final frame sent and completion status received, final result selected using best strategy
                        # Prioritize using the latest result in recognition completion state rather than just based on length
                        if self.best_text:
                            # If the current text is received after the final frame is sent or the recognition is completed, use it first.
                            if (
                                self.last_frame_sent or status == 2
                            ) and self.text.strip():
                                logger.bind(tag=TAG).info(
                                    f"Use the latest recognition result in the completed state: {self.text}"
                                )
                            elif len(self.best_text) > len(self.text):
                                logger.bind(tag=TAG).info(
                                    f"Use longer best text as final result: {self.text} -> {self.best_text}"
                                )
                                self.text = self.best_text

                        logger.bind(tag=TAG).info(f"Get the final complete text: {self.text}")
                        conn.reset_vad_states()
                        if len(audio_data) > 15:  # Make sure there is enough audio data
                            # Prepare to process results
                            pass
                        break

                except asyncio.TimeoutError:
                    if self.last_frame_sent:
                        # Also use best text on timeout
                        if self.best_text and len(self.best_text) > len(self.text):
                            logger.bind(tag=TAG).info(
                                f"Timeout, use best text: {self.text} -> {self.best_text}"
                            )
                            self.text = self.best_text
                        logger.bind(tag=TAG).info(
                            f"Timeout after final frame, use result: {self.text}"
                        )
                        break
                    # If the final frame has not been sent yet, continue to wait.
                    continue
                except websockets.ConnectionClosed:
                    logger.bind(tag=TAG).info("ASR service connection closed")
                    self.is_processing = False
                    break
                except Exception as e:
                    logger.bind(tag=TAG).error(f"An error occurred while processing ASR results: {str(e)}")
                    if hasattr(e, "__cause__") and e.__cause__:
                        logger.bind(tag=TAG).error(f"Error reason: {str(e.__cause__)}")
                    self.is_processing = False
                    break

        except Exception as e:
            logger.bind(tag=TAG).error(f"An error occurred in the ASR result forwarding task: {str(e)}")
            if hasattr(e, "__cause__") and e.__cause__:
                logger.bind(tag=TAG).error(f"Error reason: {str(e.__cause__)}")
        finally:
            if self.asr_ws:
                await self.asr_ws.close()
                self.asr_ws = None
            self.is_processing = False
            if conn:
                if hasattr(conn, "asr_audio_for_voiceprint"):
                    conn.asr_audio_for_voiceprint = []
                if hasattr(conn, "asr_audio"):
                    conn.asr_audio = []
                if hasattr(conn, "has_valid_voice"):
                    conn.has_valid_voice = False

    async def handle_voice_stop(self, conn, asr_audio_task: List[bytes]):
        """Handle speech stops, send last frame and process recognition results"""
        try:
            # Send the last frame first to indicate the end of the audio
            if self.asr_ws and self.is_processing:
                try:
                    # Take the last valid audio frame as the last frame data
                    last_frame = b""
                    if asr_audio_task:
                        last_audio = asr_audio_task[-1]
                        last_frame = self.decoder.decode(last_audio, 960)
                    await self._send_audio_frame(last_frame, STATUS_LAST_FRAME)
                    logger.bind(tag=TAG).info("Last frame sent")

                    # After sending the final frame, give _forward_results appropriate time to process the final result
                    await asyncio.sleep(0.25)

                    logger.bind(tag=TAG).info(f"Prepare to process the final recognition result: {self.text}")
                except Exception as e:
                    logger.bind(tag=TAG).error(f"Failed to send last frame: {e}")

            # Call the handle_voice_stop method of the parent class to process the recognition result
            await super().handle_voice_stop(conn, asr_audio_task)
        except Exception as e:
            logger.bind(tag=TAG).error(f"Failed to handle speech stop: {e}")
            import traceback

            logger.bind(tag=TAG).debug(f"Exception details: {traceback.format_exc()}")

    def stop_ws_connection(self):
        if self.asr_ws:
            asyncio.create_task(self.asr_ws.close())
            self.asr_ws = None
        self.is_processing = False

    async def _cleanup(self, conn):
        """Clean up resources"""
        logger.bind(tag=TAG).info(
            f"Start ASR session cleanup | Current status: processing={self.is_processing}, server_ready={self.server_ready}"
        )

        # send last frame
        if self.asr_ws and self.is_processing:
            try:
                await self._send_audio_frame(b"", STATUS_LAST_FRAME)
                await asyncio.sleep(0.1)
                logger.bind(tag=TAG).info("Last frame sent")
            except Exception as e:
                logger.bind(tag=TAG).error(f"Failed to send last frame: {e}")

        # status reset
        self.is_processing = False
        self.server_ready = False
        self.last_frame_sent = False
        self.best_text = ""
        self.has_final_result = False
        logger.bind(tag=TAG).info("ASR status has been reset")

        # Cleanup tasks
        if self.forward_task and not self.forward_task.done():
            self.forward_task.cancel()
            try:
                await asyncio.wait_for(self.forward_task, timeout=1.0)
            except asyncio.CancelledError:
                pass
            except Exception as e:
                logger.bind(tag=TAG).debug(f"forward_task cancellation exception: {e}")
            finally:
                self.forward_task = None

        # close connection
        if self.asr_ws:
            try:
                logger.bind(tag=TAG).debug("Closing WebSocket connection")
                await asyncio.wait_for(self.asr_ws.close(), timeout=2.0)
                logger.bind(tag=TAG).debug("WebSocket connection closed")
            except Exception as e:
                logger.bind(tag=TAG).error(f"Failed to close WebSocket connection: {e}")
            finally:
                self.asr_ws = None

        # Clear connected audio cache
        if conn:
            if hasattr(conn, "asr_audio_for_voiceprint"):
                conn.asr_audio_for_voiceprint = []
            if hasattr(conn, "asr_audio"):
                conn.asr_audio = []
            if hasattr(conn, "has_valid_voice"):
                conn.has_valid_voice = False

        logger.bind(tag=TAG).info("ASR session cleanup completed")

    async def speech_to_text(self, opus_data, session_id, audio_format):
        """Get recognition results"""
        result = self.text
        self.text = ""
        return result, None

    async def close(self):
        """Resource cleanup method"""
        if self.asr_ws:
            await self.asr_ws.close()
            self.asr_ws = None
        if self.forward_task:
            self.forward_task.cancel()
            try:
                await self.forward_task
            except asyncio.CancelledError:
                pass
            self.forward_task = None
        self.is_processing = False
        # Clear all connected audio buffers
        if hasattr(self, "_connections"):
            for conn in self._connections.values():
                if hasattr(conn, "asr_audio_for_voiceprint"):
                    conn.asr_audio_for_voiceprint = []
                if hasattr(conn, "asr_audio"):
                    conn.asr_audio = []
                if hasattr(conn, "has_valid_voice"):
                    conn.has_valid_voice = False
