"""Configuration management for DebateShield Lite"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM
    LLM_API_KEY = os.getenv("LLM_API_KEY", "")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4-turbo-preview")
    
    # You.com
    YOU_API_KEY = os.getenv("YOU_API_KEY", "")
    
    # Intercom
    INTERCOM_TOKEN = os.getenv("INTERCOM_TOKEN", "")
    INTERCOM_TARGET_ID = os.getenv("INTERCOM_TARGET_ID", "")
    
    # Plivo
    PLIVO_AUTH_ID = os.getenv("PLIVO_AUTH_ID", "")
    PLIVO_AUTH_TOKEN = os.getenv("PLIVO_AUTH_TOKEN", "")
    PLIVO_FROM_NUMBER = os.getenv("PLIVO_FROM_NUMBER", "")
    PLIVO_TO_NUMBER = os.getenv("PLIVO_TO_NUMBER", "")
    
    # App
    APP_ENV = os.getenv("APP_ENV", "dev")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "./debateshield.db")
    
    @classmethod
    def validate(cls):
        """Check if required keys are present"""
        missing = []
        if not cls.LLM_API_KEY:
            missing.append("LLM_API_KEY")
        if not cls.YOU_API_KEY:
            missing.append("YOU_API_KEY")
        
        if missing:
            print(f"⚠️  Warning: Missing config keys: {', '.join(missing)}")
            print("   Some features may not work without proper API keys")
        
        return len(missing) == 0

config = Config()
