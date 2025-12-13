from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra='ignore'
    )
    # Qdrant Settings
    QDRANT_HOST: str 
    QDRANT_PORT: int 
    QDRANT_API_KEY: str 

    # Embedding Settings
    EMBEDDING_BASE_URL: str 
    EMBEDDING_MODEL: str 
    EMBEDDING_DIM: int 

    # Retriever Settings 
    RERANKER_MODEL_NAME: str 
    
    # llm
    LLM_BASE_URL: str 
    LLM_MODEL_NAME: str 
    
    # General 
    MAX_CONTEXT_CHUNKS: int = 8

settings = Settings() 
print("Loaded:", settings.QDRANT_HOST, settings.QDRANT_PORT)