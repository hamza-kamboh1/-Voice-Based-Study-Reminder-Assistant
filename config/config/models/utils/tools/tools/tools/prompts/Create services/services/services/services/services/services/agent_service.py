"""
Agent Service - Main orchestration of voice AI pipeline
"""
from typing import Optional
from utils.logger import logger
from config.constants import SystemMessages
from services.stt_service import STTService
from services.tts_service import TTSService
from services.llm_service import LLMService
from services.memory_service import ConversationMemory
from services.audio_service import AudioService

class AgentService:
    def __init__(self):
        self.stt = STTService()
        self.tts = TTSService()
        self.llm = LLMService()
        self.memory = ConversationMemory(max_history=10)
        self.audio = AudioService()
        
        self.system_prompt = self._load_system_prompt()
        logger.info("Agent Service initialized successfully")
    
    def _load_system_prompt(self) -> str:
        try:
            with open('prompts/system_prompt.txt', 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error loading system prompt: {e}")
            return "You are a helpful assistant."
    
    def process_voice_input(self, audio_data: bytes) -> Optional[str]:
        try:
            text = self.stt.transcribe_audio(audio_data)
            if not text:
                return None
            
            logger.info(f"User said: {text}")
            self.memory.add_message("user", text)
            
            response = self.llm.process_with_tools(
                self.memory.get_history(),
                self.system_prompt
            )
            
            response_text = response.get('content', 'I processed your request but have no response.')
            if not response_text:
                response_text = "I processed your request successfully."
            
            self.memory.add_message("assistant", response_text)
            logger.info(f"Assistant response: {response_text[:50]}...")
            return response_text
        except Exception as e:
            logger.error(f"Error processing voice input: {e}")
            return SystemMessages.ERROR
    
    def process_text_input(self, text: str) -> Optional[str]:
        try:
            self.memory.add_message("user", text)
            
            response = self.llm.process_with_tools(
                self.memory.get_history(),
                self.system_prompt
            )
            
            response_text = response.get('content', 'I processed your request but have no response.')
            if not response_text:
                response_text = "I processed your request successfully."
            
            self.memory.add_message("assistant", response_text)
            return response_text
        except Exception as e:
            logger.error(f"Error processing text input: {e}")
            return SystemMessages.ERROR
    
    def speak_response(self, text: str) -> bool:
        try:
            audio_data = self.tts.text_to_speech(text)
            if audio_data:
                return self.audio.play_audio(audio_data)
            else:
                logger.error("Failed to generate TTS audio")
                return False
        except Exception as e:
            logger.error(f"Error speaking response: {e}")
            return False
    
    def start_conversation(self):
        logger.info("Starting conversation mode...")
        print("\n" + SystemMessages.WELCOME)
        print("Say 'goodbye' or 'exit' to end the conversation.\n")
        
        self.speak_response(SystemMessages.WELCOME)
        
        while True:
            try:
                print("\n🎤 Listening... (speak now)")
                text = self.stt.transcribe_from_microphone()
                
                if text:
                    print(f"\n👤 You said: {text}")
                    
                    if text.lower() in ['goodbye', 'exit', 'quit', 'bye']:
                        print("\n👋 Goodbye!")
                        self.speak_response(SystemMessages.GOODBYE)
                        break
                    
                    response = self.process_text_input(text)
                    if response:
                        print(f"\n🤖 Assistant: {response}")
                        self.speak_response(response)
                else:
                    print("\n⏳ No speech detected. Try again.")
            except KeyboardInterrupt:
                print("\n\n👋 Conversation ended.")
                self.speak_response(SystemMessages.GOODBYE)
                break
            except Exception as e:
                logger.error(f"Error in conversation loop: {e}")
                print(f"\n⚠️ Error: {e}")
    
    def close(self):
        self.audio.close()
        logger.info("Agent service closed")