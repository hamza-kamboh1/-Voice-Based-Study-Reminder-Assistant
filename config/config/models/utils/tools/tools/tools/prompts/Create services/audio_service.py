"""
Audio Service - Handles microphone input and speaker output using sounddevice
"""
import sounddevice as sd
import numpy as np
import wave
import io
from typing import Optional
from pydub import AudioSegment
from pydub.playback import play
from utils.logger import logger
from config.settings import Config
import tempfile
import os

class AudioService:
    def __init__(self):
        self.sample_rate = Config.AUDIO_SAMPLE_RATE
        self.channels = Config.AUDIO_CHANNELS
        self.chunk = Config.AUDIO_CHUNK
        
        # Get device info
        try:
            self.devices = sd.query_devices()
            logger.info(f"Audio Service initialized. Available devices: {len(self.devices)}")
        except Exception as e:
            logger.warning(f"Could not query audio devices: {e}")
    
    def record_audio(self, duration: float = 5.0) -> Optional[bytes]:
        """Record audio from microphone for specified duration"""
        try:
            logger.info(f"Recording audio for {duration} seconds...")
            
            # Record audio
            recording = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype='int16'
            )
            sd.wait()  # Wait until recording is finished
            
            # Convert to bytes
            audio_data = recording.tobytes()
            logger.info(f"Recorded {len(audio_data)} bytes of audio")
            return audio_data
            
        except Exception as e:
            logger.error(f"Error recording audio: {e}")
            return None
    
    def play_audio(self, audio_data: bytes) -> bool:
        """Play audio through speakers"""
        try:
            # Convert bytes to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            # Play audio
            sd.play(audio_array, samplerate=self.sample_rate)
            sd.wait()
            logger.info(f"Played {len(audio_data)} bytes of audio")
            return True
            
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
            return False
    
    def save_audio(self, audio_data: bytes, filename: str) -> bool:
        """Save audio to WAV file"""
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data)
            logger.info(f"Saved audio to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving audio: {e}")
            return False
    
    def close(self):
        """Close audio resources"""
        logger.info("Audio service closed")