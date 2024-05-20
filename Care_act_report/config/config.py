import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Configuration for file paths and settings
    DETAILS_PATH = os.getenv('DETAILS_PATH')
    BASE_DATA_PATH = os.getenv('BASE_DATA_PATH')
    IMAGE_DIR = os.getenv('IMAGE_DIR')
    REPORT_DIR = os.getenv('REPORT_DIR')
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USER = 'aravindhant7@gmail.com'
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    HEADER_IMAGE = os.getenv('HEADER_IMAGE')
    FOOTER_IMAGE = os.getenv('FOOTER_IMAGE')
    REPORT_TIMEFRAME = 'quarterly'
    DIRECTORY = os.getenv('Directory')
    LOG_DIR = os.getenv('Log')

    @staticmethod
    def ensure_directories():
        """Ensure necessary directories exist."""
        os.makedirs(Config.IMAGE_DIR, exist_ok=True)
        os.makedirs(Config.REPORT_DIR, exist_ok=True)
        os.makedirs(Config.LOG_DIR, exist_ok=True)
