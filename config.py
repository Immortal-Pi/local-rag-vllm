from pydantic import BaseSettings, Field 

class Settings(BaseSettings):
    
    # Qdrant Settings
    QDRANT_HOST: str = Field(..., env="QDRANT_HOST")
    QDRANT_PORT: int = Field(..., env="QDRANT_PORT")
    QDRANT_API_KEY: str = Field(..., env="QDRANT_API_KEY")

    # Embedding Settings 
    EMBEDDING_MODEL: str = Field(..., env="EMBEDDING_MODEL")
    EMBEDDING_DIM: int = Field(..., env="EMBEDDING_DIM")

    # Retriever Settings 
    RETRIEVER_MODEL_NAME: str = Field(..., env="RETRIEVER_MODEL_NAME")
    
    # vllm
    VLLM_BASE_URL: str = Field(..., env="VLLM_BASE_URL")
    VLLM_MODEL_NAME: str = Field(..., env="VLLM_MODEL_NAME")
    
    # General 
    MAX_CONTEXT_CHUNKS: int = 8

    class Config:
        env_file = ".env"

settings = Settings() 