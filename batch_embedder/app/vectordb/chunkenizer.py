from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.settings import get_settings
from core.logger import logger

def recursive_character_splitting(text: str, chunk_size: int = None, chunk_overlap: int = None) -> list:
    """Split text into chunks using recursive character text splitter"""
    settings = get_settings()
    
    # Use provided parameters or fall back to settings
    chunk_size = chunk_size or settings.CHUNK_SIZE
    chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_text(text)
    logger.info(f"Split text into {len(chunks)} chunks (chunk_size={chunk_size}, overlap={chunk_overlap})")
    return chunks