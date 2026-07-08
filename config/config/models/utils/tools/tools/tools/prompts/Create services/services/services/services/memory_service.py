"""
Memory Service - Handles conversation memory
"""
from typing import List, Dict
from datetime import datetime
from utils.logger import logger

class ConversationMemory:
    def __init__(self, max_history: int = 10):
        self.messages: List[Dict] = []
        self.max_history = max_history
        
    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
        logger.debug(f"Added {role} message: {content[:50]}...")
    
    def get_history(self) -> List[Dict]:
        return [{"role": m["role"], "content": m["content"]} for m in self.messages]
    
    def clear(self):
        self.messages.clear()
        logger.info("Conversation memory cleared")