from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY: str = environ.get("OPENAI_API_KEY", "")
    CHAT_MODEL_ID: str = environ.get("CHAT_MODEL_ID", "gpt-4o-mini")
    
    # Qdrant Configuration
    QDRANT_URL: str = environ.get("QDRANT_URL", "http://localhost:6333")
    
    # Collections Configuration
    COLLECTIONS = {
        "hr_policies": "hr_policies",
        "labor_rules": "labor_rules", 
        "product_manual": "product_manual"
    }
    
    # Team Configuration
    NUM_DOCUMENTS: int = int(environ.get("NUM_DOCUMENTS", "4"))
    NUM_HISTORY_RUNS: int = int(environ.get("NUM_HISTORY_RUNS", "5"))
    ENABLE_STREAMING: bool = environ.get("ENABLE_STREAMING", "true").lower() == "true"
    
    # Debug Configuration
    DEBUG_MODE: bool = environ.get("DEBUG_MODE", "false").lower() == "true"
    SHOW_MEMBERS_RESPONSES: bool = environ.get("SHOW_MEMBERS_RESPONSES", "true").lower() == "true"

def get_settings():
    return Config() 