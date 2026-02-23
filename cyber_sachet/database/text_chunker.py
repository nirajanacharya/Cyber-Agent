"""Text chunking utilities."""

from typing import List


def chunk_text(content: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        content: Text content to chunk
        chunk_size: Size of each chunk in characters
        chunk_overlap: Number of overlapping characters between chunks
    
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    
    while start < len(content):
        end = start + chunk_size
        chunk = content[start:end]
        
        if end < len(content):
            last_period = chunk.rfind(". ")
            if last_period > chunk_size // 2:
                end = start + last_period + 1
                chunk = content[start:end]
        
        chunk_stripped = chunk.strip()
        if chunk_stripped:
            chunks.append(chunk_stripped)
        
        start = end - chunk_overlap
    
    return chunks
