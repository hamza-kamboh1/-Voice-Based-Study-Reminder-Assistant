"""
STT Service - Pure sounddevice implementation (No PyAudio)
"""
import sounddevice as sd
import speech_recognition as sr
import numpy as np
from typing import Optional
from utils.logger import logger

class STTService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.sample_rate = 16000
        self.channels = 1
        self.duration = 5
        logger.info("✅ STT Service ready (using sounddevice)")
    
    def transcribe_from_microphone(self) -> Optional[str]:
        """Record and transcribe using only sounddevice"""
        try:
            print("\n🎤 Recording... Speak now!")
            
            # Record using sounddevice
            recording = sd.rec(
                int(self.duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype='int16'
            )
            sd.wait()
            
            # Convert to AudioData
            audio_data = recording.tobytes()
            audio = sr.AudioData(audio_data, self.sample_rate, 2)
            
            # Transcribe using Google
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Transcribed: {text}")
            return text
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Google STT error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
