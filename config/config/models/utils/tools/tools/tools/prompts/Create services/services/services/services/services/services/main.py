"""
LifeKit - Voice AI Assistant
Main application entry point
"""

import sys
import time
from utils.logger import logger
from config.settings import Config
from config.constants import SystemMessages
from services.agent_service import AgentService

def main():
    """Main application entry point"""
    logger.info("=" * 60)
    logger.info("Starting LifeKit Voice AI Assistant...")
    logger.info(f"Using LLM Model: {Config.LLM_MODEL}")
    logger.info(f"Log Level: {Config.LOG_LEVEL}")
    logger.info("=" * 60)
    
    agent = None
    try:
        agent = AgentService()
        print("\n🎯 LifeKit Voice AI Assistant is ready!")
        print("=" * 50)
        print("Commands:")
        print("  - Speak naturally to add, list, complete, or delete tasks")
        print("  - Say 'goodbye' or 'exit' to quit")
        print("=" * 50)
        
        agent.start_conversation()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Happy studying!" if agent else "\n\nExiting...")
        logger.info("Application interrupted by user")
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"\n❌ Error: {e}")
        print("Please check the logs for more details.")
        
    finally:
        if agent:
            agent.close()
        logger.info("LifeKit shutdown complete.")
        logger.info("=" * 60)

if __name__ == "__main__":
    main()