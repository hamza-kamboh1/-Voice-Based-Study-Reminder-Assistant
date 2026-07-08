"""
Speech-to-Text Service - Converts audio to text
"""
import speech_recognition as sr
from typing import Optional
from utils.logger import logger

class STTService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        logger.info("STT Service initialized")
    
    def transcribe_audio(self, audio_data: bytes) -> Optional[str]:
        try:
            audio = sr.AudioData(audio_data, 16000, 2)
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Transcribed: {text}")
            return text
        except sr.UnknownValueError:
            logger.warning("Speech recognition could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Error with speech recognition service: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in STT: {e}")
            return None
    
    def transcribe_from_microphone(self) -> Optional[str]:
        try:
            with sr.Microphone() as source:
                logger.info("Listening for speech...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                logger.info("Processing speech...")
                text = self.recognizer.recognize_google(audio)
                logger.info(f"Transcribed: {text}")
                return text
        except sr.WaitTimeoutError:
            logger.warning("Listening timeout - no speech detected")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except Exception as e:
            logger.error(f"Error in microphone transcription: {e}")
            return None