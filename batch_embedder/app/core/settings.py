from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY: str = environ.get("OPENAI_API_KEY_2", "")
    EMBEDDING_MODEL: str = environ.get("EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Qdrant Configuration
    QDRANT_URL: str = environ.get("QDRANT_URL", "http://localhost:6333")
    
    # Data Configuration
    DATA_PATH: str = environ.get("DATA_PATH", "./data")
    
    # Collections Configuration
    COLLECTIONS = {
        "hr-policies": "hr_policies",
        "labor-rules": "labor_rules", 
        "product-manual": "product_manual"
    }
    
    # Chunking Configuration
    CHUNK_SIZE: int = int(environ.get("CHUNK_SIZE", "300"))
    CHUNK_OVERLAP: int = int(environ.get("CHUNK_OVERLAP", "20"))

def get_settings():
    return Config()
