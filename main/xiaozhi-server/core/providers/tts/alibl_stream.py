import os
import uuid
import json
import time
import queue
import asyncio
import traceback
import websockets
from asyncio import Task
from config.logger import setup_logging
from core.utils import opus_encoder_utils
from core.utils.tts import MarkdownCleaner
from core.providers.tts.base import TTSProviderBase
from core.providers.tts.dto.dto import SentenceType, ContentType, InterfaceType

TAG = __name__
logger = setup_logging()


class TTSProvider(TTSProviderBase):
    def __init__(self, config, delete_audio_file):
        super().__init__(config, delete_audio_file)

        self.interface_type = InterfaceType.DUAL_STREAM
        # Basic configuration
        self.api_key = config.get("api_key")
        if not self.api_key:
            raise ValueError("api_key is required for CosyVoice TTS")

        # WebSocket configuration
        self.ws_url = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/"
        self.ws = None
        self._monitor_task = None
        self.last_active_time = None

        # Model and tone configuration
        self.model = config.get("model", "cosyvoice-v2")
        self.voice = config.get("voice", "longxiaochun_v2")  # Default sound
        if config.get("private_voice"):
            self.voice = config.get("private_voice")

        # Audio parameter configuration
        self.format = config.get("format", "pcm")
        sample_rate = config.get("sample_rate", "24000")
        self.sample_rate = int(sample_rate) if sample_rate else 24000

        volume = config.get("volume", "50")
        self.volume = int(volume) if volume else 50

        rate = config.get("rate", "1.0")
        self.rate = float(rate) if rate else 1.0

        pitch = config.get("pitch", "1.0")
        self.pitch = float(pitch) if pitch else 1.0

        self.header = {
            "Authorization": f"Bearer {self.api_key}",
            # "user-agent": "your_platform_info", // optional
            # "X-DashScope-WorkSpace": workspace, // Optional, Alibaba Cloud Bailian business space ID
            "X-DashScope-DataInspection": "enable",
        }

        # Create Opus encoder
        self.opus_encoder = opus_encoder_utils.OpusEncoderUtils(
            sample_rate=self.sample_rate, channels=1, frame_size_ms=60
        )

    async def _ensure_connection(self):
        """Ensure that the WebSocket connection is available and support connection reuse within 60 seconds"""
        try:
            current_time = time.time()
            if self.ws and current_time - self.last_active_time < 60:
                # The link can be reused for continuous conversations within one minute.
                logger.bind(tag=TAG).info(f"Use existing link...")
                return self.ws
            logger.bind(tag=TAG).info("Starting a new connection...")

            self.ws = await websockets.connect(
                self.ws_url,
                additional_headers=self.header,
                ping_interval=30,
                ping_timeout=10,
                close_timeout=10,
            )

            logger.bind(tag=TAG).info("WebSocket connection established successfully")
            self.last_active_time = current_time
            return self.ws
        except Exception as e:
            logger.bind(tag=TAG).error(f"Failed to establish connection: {str(e)}")
            self.ws = None
            self.last_active_time = None
            raise

    def tts_text_priority_thread(self):
        """Streaming TTS text processing thread"""
        while not self.conn.stop_event.is_set():
            try:
                message = self.tts_text_queue.get(timeout=1)
                logger.bind(tag=TAG).debug(
                    f"Received TTS task | {message.sentence_type.name} | {message.content_type.name} | Session ID: {self.conn.sentence_id}"
                )

                if message.sentence_type == SentenceType.FIRST:
                    self.conn.client_abort = False

                if self.conn.client_abort:
                    try:
                        logger.bind(tag=TAG).info("Receive interrupt message, terminate TTS text processing thread")
                        continue
                    except Exception as e:
                        logger.bind(tag=TAG).error(f"Failed to cancel TTS session: {str(e)}")
                        continue

                if message.sentence_type == SentenceType.FIRST:
                    # Initialize session
                    try:
                        if not getattr(self.conn, "sentence_id", None): 
                            self.conn.sentence_id = uuid.uuid4().hex
                            logger.bind(tag=TAG).info(f"Automatically generate a new session ID: {self.conn.sentence_id}")

                        logger.bind(tag=TAG).info("Starting a TTS session...")
                        future = asyncio.run_coroutine_threadsafe(
                            self.start_session(self.conn.sentence_id),
                            loop=self.conn.loop,
                        )
                        future.result()
                        self.before_stop_play_files.clear()
                        logger.bind(tag=TAG).info("TTS session started successfully")
                    except Exception as e:
                        logger.bind(tag=TAG).error(f"Failed to start TTS session: {str(e)}")
                        continue

                elif ContentType.TEXT == message.content_type:
                    if message.content_detail:
                        try:
                            logger.bind(tag=TAG).debug(
                                f"Start sending TTS text: {message.content_detail}"
                            )
                            future = asyncio.run_coroutine_threadsafe(
                                self.text_to_speak(message.content_detail, None),
                                loop=self.conn.loop,
                            )
                            future.result()
                            logger.bind(tag=TAG).debug("TTS text sent successfully")
                        except Exception as e:
                            logger.bind(tag=TAG).error(f"Failed to send TTS text: {str(e)}")
                            continue

                elif ContentType.FILE == message.content_type:
                    logger.bind(tag=TAG).info(
                        f"Add audio files to the playlist: {message.content_file}"
                    )
                    if message.content_file and os.path.exists(message.content_file):
                        # Process the file audio data first
                        self._process_audio_file_stream(message.content_file, callback=lambda audio_data: self.handle_audio_file(audio_data, message.content_detail))

                if message.sentence_type == SentenceType.LAST:
                    try:
                        logger.bind(tag=TAG).info("Start ending TTS session...")
                        future = asyncio.run_coroutine_threadsafe(
                            self.finish_session(self.conn.sentence_id),
                            loop=self.conn.loop,
                        )
                        future.result()
                    except Exception as e:
                        logger.bind(tag=TAG).error(f"Failed to end TTS session: {str(e)}")
                        continue

            except queue.Empty:
                continue
            except Exception as e:
                logger.bind(tag=TAG).error(
                    f"Failed to process TTS text: {str(e)}, type: {type(e).__name__}, stack: {traceback.format_exc()}"
                )
                continue

    async def text_to_speak(self, text, _):
        """Send text to TTS service for composition"""
        try:
            if self.ws is None:
                logger.bind(tag=TAG).warning("WebSocket connection does not exist, terminate sending text")
                return

            # Filter Markdown
            filtered_text = MarkdownCleaner.clean_markdown(text)

            # Send continue-task message
            continue_task_message = {
                "header": {
                    "action": "continue-task",
                    "task_id": self.conn.sentence_id,
                    "streaming": "duplex",
                },
                "payload": {"input": {"text": filtered_text}},
            }

            await self.ws.send(json.dumps(continue_task_message))
            self.last_active_time = time.time()
            logger.bind(tag=TAG).debug(f"Sent text: {filtered_text}")

        except Exception as e:
            logger.bind(tag=TAG).error(f"Failed to send TTS text: {str(e)}")
            if self.ws:
                try:
                    await self.ws.close()
                except:
                    pass
                self.ws = None
            raise

    async def start_session(self, session_id):
        """Start TTS session"""
        logger.bind(tag=TAG).info(f"Start session~~{session_id}")
        try:
            # Check and clean up the listening tasks of the previous session
            if (
                self._monitor_task is not None
                and isinstance(self._monitor_task, Task)
                and not self._monitor_task.done()
            ):
                logger.bind(tag=TAG).info("An unfinished last session was detected and the listening task was closed...")
                await self.close()

            # Make sure the connection is available
            await self._ensure_connection()

            # Start listening task
            self._monitor_task = asyncio.create_task(self._start_monitor_tts_response())

            # Send a run-task message to start the session
            run_task_message = {
                "header": {
                    "action": "run-task",
                    "task_id": session_id,
                    "streaming": "duplex",
                },
                "payload": {
                    "task_group": "audio",
                    "task": "tts",
                    "function": "SpeechSynthesizer",
                    "model": self.model,
                    "parameters": {
                        "text_type": "PlainText",
                        "voice": self.voice,
                        "format": self.format,
                        "sample_rate": self.sample_rate,
                        "volume": self.volume,
                        "rate": self.rate,
                        "pitch": self.pitch,
                    },
                    "input": {}
                },
            }

            await self.ws.send(json.dumps(run_task_message))
            self.last_active_time = time.time()
            logger.bind(tag=TAG).info("Session start request sent")
        except Exception as e:
            logger.bind(tag=TAG).error(f"Failed to start session: {str(e)}")
            await self.close()
            raise

    async def finish_session(self, session_id):
        """End TTS session"""
        logger.bind(tag=TAG).info(f"Close session~~{session_id}")
        try:
            if self.ws and session_id:
                # Send finish-task message
                finish_task_message = {
                    "header": {
                        "action": "finish-task",
                        "task_id": session_id,
                        "streaming": "duplex",
                    },
                    "payload": {
                        "input": {}
                    }
                }

                await self.ws.send(json.dumps(finish_task_message))
                self.last_active_time = time.time()
                logger.bind(tag=TAG).info("Session end request sent")
                # Wait for the listening task to complete
                if self._monitor_task:
                    try:
                        await self._monitor_task
                    except Exception as e:
                        logger.bind(tag=TAG).error(
                            f"An error occurred while waiting for the listening task to complete: {str(e)}"
                        )
                    finally:
                        self._monitor_task = None

        except Exception as e:
            logger.bind(tag=TAG).error(f"Failed to close session: {str(e)}")
            await self.close()
            raise

    async def close(self):
        """Clean up resources"""
        # Cancel monitoring task
        if self._monitor_task:
            try:
                self._monitor_task.cancel()
                await self._monitor_task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                logger.bind(tag=TAG).warning(f"Error in canceling listening task when closing: {e}")
            self._monitor_task = None

        # Close WebSocket connection
        if self.ws:
            try:
                await self.ws.close()
            except:
                pass
            self.ws = None
            self.last_active_time = None

    async def _start_monitor_tts_response(self):
        """Listen for TTS responses"""
        try:
            session_finished = False
            while not self.conn.stop_event.is_set():
                try:
                    msg = await self.ws.recv()
                    self.last_active_time = time.time()

                    # Check if client aborted
                    if self.conn.client_abort:
                        logger.bind(tag=TAG).info("After receiving the interrupt message, stop monitoring the TTS response.")
                        break

                    if isinstance(msg, str):  # JSON control message
                        try:
                            data = json.loads(msg)
                            event = data["header"].get("event")

                            if event == "task-started":
                                logger.bind(tag=TAG).debug("TTS task started successfully~")
                                self.tts_audio_queue.put((SentenceType.FIRST, [], None))
                            elif event == "result-generated":
                                # Send cached data
                                if self.conn.tts_MessageText:
                                    logger.bind(tag=TAG).info(
                                        f"Sentence speech generation successful: {self.conn.tts_MessageText}"
                                    )
                                    self.tts_audio_queue.put(
                                        (SentenceType.FIRST, [], self.conn.tts_MessageText)
                                    )
                                    self.conn.tts_MessageText = None
                            elif event == "task-finished":
                                logger.bind(tag=TAG).debug("TTS mission completed~")
                                self._process_before_stop_play_files()
                                session_finished = True
                                break
                            elif event == "task-failed":
                                error_code = data["header"].get("error_code", "unknown")
                                error_message = data["header"].get("error_message", "unknown error")
                                logger.bind(tag=TAG).error(
                                    f"TTS task failed: {error_code} - {error_message}"
                                )
                                break
                        except json.JSONDecodeError:
                            logger.bind(tag=TAG).warning("Invalid JSON message received")
                    elif isinstance(msg, (bytes, bytearray)):
                        self.opus_encoder.encode_pcm_to_opus_stream(
                            msg, False, callback=self.handle_opus
                        )
                except websockets.ConnectionClosed:
                    logger.bind(tag=TAG).warning("WebSocket connection closed")
                    break
                except Exception as e:
                    logger.bind(tag=TAG).error(
                        f"Error while processing TTS response: {e}\n{traceback.format_exc()}"
                    )
                    break

            # Only close the connection when the connection is abnormal and ends abnormally
            if not session_finished and self.ws:
                try:
                    await self.ws.close()
                except:
                    pass
                self.ws = None
        # Clean up references when the listening task exits
        finally:
            self._monitor_task = None

    def to_tts(self, text: str) -> list:
        """Non-streaming generated audio data, used to generate audio and test scenarios"""
        try:
            # Create event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Generate session ID
            session_id = uuid.uuid4().hex
            # Store audio data
            audio_data = []

            async def _generate_audio():
                ws = await websockets.connect(
                    self.ws_url,
                    additional_headers=self.header,
                    ping_interval=30,
                    ping_timeout=10,
                    close_timeout=10,
                    max_size=10 * 1024 * 1024,
                )

                try:
                    # Send a run-task message to start the session
                    run_task_message = {
                        "header": {
                            "action": "run-task",
                            "task_id": session_id,
                            "streaming": "duplex",
                        },
                        "payload": {
                            "task_group": "audio",
                            "task": "tts",
                            "function": "SpeechSynthesizer",
                            "model": self.model,
                            "parameters": {
                                "text_type": "PlainText",
                                "voice": self.voice,
                                "format": self.format,
                                "sample_rate": self.sample_rate,
                                "volume": self.volume,
                                "rate": self.rate,
                                "pitch": self.pitch,
                            },
                            "input": {}
                        },
                    }
                    await ws.send(json.dumps(run_task_message))

                    # Wait for task to start
                    task_started = False
                    while not task_started:
                        msg = await ws.recv()
                        if isinstance(msg, str):
                            data = json.loads(msg)
                            header = data.get("header", {})
                            if header.get("event") == "task-started":
                                task_started = True
                                logger.bind(tag=TAG).debug("TTS task has been started")
                            elif header.get("event") == "task-failed":
                                error_code = header.get("error_code", "unknown")
                                error_message = header.get("error_message", "unknown error")
                                raise Exception(
                                    f"Failed to start task: {error_code} - {error_message}"
                                )

                    # Send text
                    filtered_text = MarkdownCleaner.clean_markdown(text)
                    # Send continue-task message
                    continue_task_message = {
                        "header": {
                            "action": "continue-task",
                            "task_id": session_id,
                            "streaming": "duplex",
                        },
                        "payload": {"input": {"text": filtered_text}},
                    }
                    await ws.send(json.dumps(continue_task_message))

                    # Send finish-task message
                    finish_task_message = {
                        "header": {
                            "action": "finish-task",
                            "task_id": session_id,
                            "streaming": "duplex",
                        },
                        "payload": {
                            "input": {}
                        }
                    }
                    await ws.send(json.dumps(finish_task_message))

                    # Receive audio data
                    task_finished = False
                    while not task_finished:
                        msg = await ws.recv()
                        if isinstance(msg, (bytes, bytearray)):
                            self.opus_encoder.encode_pcm_to_opus_stream(
                                msg,
                                end_of_stream=False,
                                callback=lambda opus: audio_data.append(opus)
                            )
                        elif isinstance(msg, str):
                            data = json.loads(msg)
                            header = data.get("header", {})
                            if header.get("event") == "task-finished":
                                task_finished = True
                                logger.bind(tag=TAG).debug("TTS mission completed")
                            elif header.get("event") == "task-failed":
                                error_code = header.get("error_code", "unknown")
                                error_message = header.get("error_message", "unknown error")
                                raise Exception(
                                    f"Synthesis failed: {error_code} - {error_message}"
                                )

                finally:
                    # Clean up resources
                    try:
                        await ws.close()
                    except:
                        pass

            # Run asynchronous tasks
            loop.run_until_complete(_generate_audio())
            loop.close()

            return audio_data

        except Exception as e:
            logger.bind(tag=TAG).error(f"Failed to generate audio data: {str(e)}")
            return []
