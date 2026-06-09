"""Logger configuration"""

import logging
import os
from config.settings import LOG_LEVEL, LOG_DIR


class Logger:
    """Logger class for application logging"""
    
    @staticmethod
    def get_logger(name=None):
        """Get logger instance"""
        logger = logging.getLogger(name or __name__)
        
        # Create logs directory if it doesn't exist
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        
        # Set log level
        logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # Remove existing handlers to avoid duplicates
        if logger.hasHandlers():
            return logger
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, LOG_LEVEL))
        
        # File handler
        log_file = os.path.join(LOG_DIR, 'test_execution.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, LOG_LEVEL))
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger
