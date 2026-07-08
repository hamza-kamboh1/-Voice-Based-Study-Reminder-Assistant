"""
Text-to-Speech Service - Converts text to audio
"""
import pyttsx3
import io
from typing import Optional
from utils.logger import logger
from config.settings import Config

class TTSService:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', Config.TTS_RATE)
        self.voices = self.engine.getProperty('voices')
        if self.voices:
            self.engine.setProperty('voice', self.voices[0].id)
        logger.info(f"TTS Service initialized with {len(self.voices)} voices")
    
    def text_to_speech(self, text: str, save_to_file: Optional[str] = None) -> Optional[bytes]:
        try:
            import tempfile
            import os
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                temp_path = tmp_file.name
            self.engine.save_to_file(text, temp_path)
            self.engine.runAndWait()
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            os.unlink(temp_path)
            if save_to_file:
                with open(save_to_file, 'wb') as f:
                    f.write(audio_data)
                logger.info(f"Saved TTS to {save_to_file}")
            logger.info(f"Generated TTS for: {text[:50]}...")
            return audio_data
        except Exception as e:
            logger.error(f"Error in TTS: {e}")
            return None
    
    def speak(self, text: str) -> bool:
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            logger.info(f"Spoke: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Error speaking: {e}")
            return False
    
    def get_voices(self):
        return self.voices
    
    def set_voice(self, voice_id: str):
        try:
            self.engine.setProperty('voice', voice_id)
            logger.info(f"Set voice to: {voice_id}")
            return True
        except Exception as e:
            logger.error(f"Error setting voice: {e}")
            return False
