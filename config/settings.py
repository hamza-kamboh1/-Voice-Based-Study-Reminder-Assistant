import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.7))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 150))
    
    # Audio Configuration
    AUDIO_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", 16000))
    AUDIO_CHANNELS = int(os.getenv("AUDIO_CHANNELS", 1))
    AUDIO_CHUNK = int(os.getenv("AUDIO_CHUNK", 1024))
    
    # TTS Configuration
    TTS_VOICE = os.getenv("TTS_VOICE", "com.apple.speech.synthesis.voice.samantha")
    TTS_RATE = int(os.getenv("TTS_RATE", 175))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
