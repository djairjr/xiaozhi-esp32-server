"""Opus coding tools
Encode PCM audio data into Opus format"""

import logging
import traceback
import numpy as np
from opuslib_next import Encoder
from opuslib_next import constants
from typing import Optional, Callable, Any

class OpusEncoderUtils:
    """PCM to Opus encoder"""

    def __init__(self, sample_rate: int, channels: int, frame_size_ms: int):
        """Initialize Opus encoder

        Args:
            sample_rate: sampling rate (Hz)
            channels: number of channels (1=mono, 2=stereo)
            frame_size_ms: frame size (milliseconds)"""
        self.sample_rate = sample_rate
        self.channels = channels
        self.frame_size_ms = frame_size_ms
        # Calculate the number of samples per frame = sampling rate * frame size (ms) / 1000
        self.frame_size = (sample_rate * frame_size_ms) // 1000
        # Total frame size = samples per frame * number of channels
        self.total_frame_size = self.frame_size * channels

        # Bitrate and complexity settings
        self.bitrate = 24000  # bps
        self.complexity = 10  # highest quality

        # The buffer is initialized empty
        self.buffer = np.array([], dtype=np.int16)

        try:
            # Create Opus encoder
            self.encoder = Encoder(
                sample_rate, channels, constants.APPLICATION_AUDIO  # Audio optimization mode
            )
            self.encoder.bitrate = self.bitrate
            self.encoder.complexity = self.complexity
            self.encoder.signal = constants.SIGNAL_VOICE  # Voice signal optimization
        except Exception as e:
            logging.error(f"Failed to initialize Opus encoder: {e}")
            raise RuntimeError("Initialization failed") from e

    def reset_state(self):
        """Reset encoder status"""
        self.encoder.reset_state()
        self.buffer = np.array([], dtype=np.int16)

    def encode_pcm_to_opus_stream(self, pcm_data: bytes, end_of_stream: bool, callback: Callable[[Any], Any]):
        """Encode PCM data into Opus format for streaming

        Args:
            pcm_data: PCM byte data
            end_of_stream: whether it is the end of the stream,
            callback: opus processing method

        Returns:
            Opus packet list"""
        # Convert byte data to short array
        new_samples = self._convert_bytes_to_shorts(pcm_data)

        # Verify PCM data
        self._validate_pcm_data(new_samples)

        # Append new data to buffer
        self.buffer = np.append(self.buffer, new_samples)

        offset = 0

        # Process all complete frames
        while offset <= len(self.buffer) - self.total_frame_size:
            frame = self.buffer[offset : offset + self.total_frame_size]
            output = self._encode(frame)
            if output:
                callback(output)
            offset += self.total_frame_size

        # Keep unprocessed samples
        self.buffer = self.buffer[offset:]

        # Process remaining data at the end of the stream
        if end_of_stream and len(self.buffer) > 0:
            # Create the last frame and fill it with 0s
            last_frame = np.zeros(self.total_frame_size, dtype=np.int16)
            last_frame[: len(self.buffer)] = self.buffer

            output = self._encode(last_frame)
            if output:
                callback(output)
            self.buffer = np.array([], dtype=np.int16)

    def _encode(self, frame: np.ndarray) -> Optional[bytes]:
        """Encode a frame of audio data"""
        try:
            # Convert numpy array to bytes
            frame_bytes = frame.tobytes()
            # opuslib requires that the number of input bytes must be a multiple of channels*2
            encoded = self.encoder.encode(frame_bytes, self.frame_size)
            return encoded
        except Exception as e:
            logging.error(f"Opus encoding failed: {e}")
            traceback.print_exc()
            return None

    def _convert_bytes_to_shorts(self, bytes_data: bytes) -> np.ndarray:
        """Convert byte array to short array (16-bit PCM)"""
        # Assuming the input is 16-bit PCM in little-endian order
        return np.frombuffer(bytes_data, dtype=np.int16)

    def _validate_pcm_data(self, pcm_shorts: np.ndarray) -> None:
        """Verify that PCM data is valid"""
        # The 16-bit PCM data range is -32768 to 32767
        if np.any((pcm_shorts < -32768) | (pcm_shorts > 32767)):
            invalid_samples = pcm_shorts[(pcm_shorts < -32768) | (pcm_shorts > 32767)]
            logging.warning(f"Invalid PCM samples found: {invalid_samples[:5]}...")
            # In practical applications, you can choose to crop instead of throwing an exception.
            # np.clip(pcm_shorts, -32768, 32767, out=pcm_shorts)

    def close(self):
        """Close the encoder and release resources"""
        # opuslib has no explicit shutdown method, Python's garbage collection will handle it
        pass