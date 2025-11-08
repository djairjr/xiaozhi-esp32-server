import os
import json
import asyncio
import tempfile
import difflib
from typing import Optional, Tuple, List
import dashscope
from config.logger import setup_logging
from core.providers.asr.base import ASRProviderBase
from core.providers.asr.dto.dto import InterfaceType

tag = __name__
logger = setup_logging()


class ASRProvider(ASRProviderBase):
    def __init__(self, config: dict, delete_audio_file: bool):
        super().__init__()
        self.interface_type = InterfaceType.STREAM
        """Qwen3-ASR-Flash ASR initialization"""
        
        # Configuration parameters
        self.api_key = config.get("api_key")
        if not self.api_key:
            raise ValueError("Qwen3-ASR-Flash needs to configure api_key")
            
        self.model_name = config.get("model_name", "qwen3-asr-flash")
        self.output_dir = config.get("output_dir", "./audio_output")
        self.delete_audio_file = delete_audio_file
        
        # ASR option configuration
        self.enable_lid = config.get("enable_lid", True)  # Automatic language detection
        self.enable_itn = config.get("enable_itn", True)  # Inverse text normalization
        self.language = config.get("language", None)  # Specify language, automatically detected by default
        self.context = config.get("context", "")  # Context information to improve recognition accuracy
        
        # Make sure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def _prepare_audio_file(self, pcm_data: bytes) -> str:
        """Convert PCM data to WAV file and return file path"""
        try:
            import wave
            
            # Create temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
                
            # Write to WAV format
            with wave.open(temp_path, 'wb') as wav_file:
                wav_file.setnchannels(1)      # mono
                wav_file.setsampwidth(2)      # 16 bit
                wav_file.setframerate(16000)  # 16kHz sampling rate
                wav_file.writeframes(pcm_data)
                
            return temp_path
            
        except Exception as e:
            logger.bind(tag=tag).error(f"Audio file preparation failed: {e}")
            return None

    async def speech_to_text(
        self, opus_data: List[bytes], session_id: str, audio_format="opus"
    ) -> Tuple[Optional[str], Optional[str]]:
        """Convert speech data to text"""
        temp_file_path = None
        file_path = None
        
        try:
            # Decode audio data
            if audio_format == "pcm":
                pcm_data = opus_data
            else:
                pcm_data = self.decode_opus(opus_data)
            
            combined_pcm_data = b"".join(pcm_data)
            if len(combined_pcm_data) == 0:
                logger.bind(tag=tag).warning("Audio data is empty")
                return "", None
            
            # Prepare audio files
            temp_file_path = self._prepare_audio_file(combined_pcm_data)
            if not temp_file_path:
                return "", None
            
            # Save audio file (if needed)
            if not self.delete_audio_file:
                file_path = self.save_audio_to_file(pcm_data, session_id)
            
            # Construct request message
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"audio": temp_file_path}
                    ]
                }
            ]
            
            # If there is context information, add system messages
            if self.context:
                messages.insert(0, {
                    "role": "system", 
                    "content": [
                        {"text": self.context}
                    ]
                })
            
            # Prepare for ASR options
            asr_options = {
                "enable_lid": self.enable_lid,
                "enable_itn": self.enable_itn
            }
            
            # If a language is specified, add it to the options
            if self.language:
                asr_options["language"] = self.language
            
            # Set API key
            dashscope.api_key = self.api_key
            
            # Send streaming request
            response = dashscope.MultiModalConversation.call(
                model=self.model_name,
                messages=messages,
                result_format="message",
                asr_options=asr_options,
                stream=True
            )
            
            # Handling streaming responses
            full_text = ""
            last_text = ""  # Used to store the previous text fragment
            for chunk in response:
                try:
                    text = chunk["output"]["choices"][0]["message"].content[0]["text"]
                    # Standardize text fragments (remove leading and trailing spaces)
                    normalized_text = text.strip()
                    # Process only if the new text fragment is different from the previous one
                    if normalized_text != last_text:
                        # Extract the new text part
                        # Find the new part by comparing the current text with the previous text
                        if normalized_text.startswith(last_text):
                            # If the current text starts with the last text, the new part is the difference between the two
                            new_part = normalized_text[len(last_text):]
                        else:
                            # If it does not start with the last text, it means that the recognition result has changed significantly, and the current text is used directly.
                            new_part = normalized_text
                        
                        # Add new parts to the complete text
                        full_text += new_part
                        last_text = normalized_text
                    # Here you can process text fragments in real time, for example through callback functions
                except:
                    pass
            
            return full_text, file_path
                
        except Exception as e:
            logger.bind(tag=tag).error(f"Speech recognition failed: {e}")
            return "", file_path
            
        finally:
            # Clean temporary files
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except Exception as e:
                    logger.bind(tag=tag).warning(f"Failed to clean up temporary files: {e}")