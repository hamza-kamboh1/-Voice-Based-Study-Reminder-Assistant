from loguru import logger
from config.settings import Config
import sys

# Configure logger
logger.remove()
logger.add(sys.stdout, level=Config.LOG_LEVEL, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")
logger.add(Config.LOG_FILE, rotation="500 MB", level=Config.LOG_LEVEL, format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}")

__all__ = ["logger"]
