"""File reading utilities."""

import os
from typing import List, Tuple


def read_text_file(filepath: str) -> str:
    """
    Read text file content.
    
    Args:
        filepath: Path to the text file
    
    Returns:
        File content as string
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def get_text_files(docs_folder: str) -> List[str]:
    """
    Get list of .txt files in a folder.
    
    Args:
        docs_folder: Path to documents folder
    
    Returns:
        List of .txt filenames
    """
    return [f for f in os.listdir(docs_folder) if f.endswith(".txt")]
