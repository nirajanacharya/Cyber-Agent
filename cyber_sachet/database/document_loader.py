"""Document loading utilities for ChromaDB."""

import os
from typing import Dict, Any

from .file_reader import read_text_file, get_text_files
from .text_chunker import chunk_text
from .doc_type_mapper import get_doc_type


def load_documents(
    collection,
    docs_folder: str = "docs/",
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> Dict[str, Any]:
    """
    Load documents from the docs folder into ChromaDB.
    
    Args:
        collection: ChromaDB collection
        docs_folder: Path to documents folder (default: "docs/")
        chunk_size: Size of text chunks (default: 500)
        chunk_overlap: Overlap between chunks (default: 100)
    
    Returns:
        Dictionary with loading statistics:
            - files_loaded: List of loaded files
            - total_chunks: Total number of chunks created
            - doc_types: Statistics by document type
    
    Example:
        >>> import chromadb
        >>> client = chromadb.Client()
        >>> collection = client.create_collection("cyber_sachet")
        >>> stats = load_documents(collection, "docs/")
        >>> print(f"Loaded {stats['total_chunks']} chunks from {len(stats['files_loaded'])} files")
    """
    documents = []
    metadatas = []
    ids = []
    chunk_counter = 0
    
    stats = {
        "files_loaded": [],
        "total_chunks": 0,
        "doc_types": {}
    }
    
    text_files = get_text_files(docs_folder)
    
    for filename in text_files:
        filepath = os.path.join(docs_folder, filename)
        
        doc_type = get_doc_type(filename)
        
        content = read_text_file(filepath)
        chunks = chunk_text(content, chunk_size, chunk_overlap)
        
        file_key = filename.replace(".txt", "")
        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({
                "source": filename,
                "doc_type": doc_type,
                "chunk_id": i,
                "total_chunks": len(chunks)
            })
            ids.append(f"{file_key}_{i}")
            chunk_counter += 1
        
        stats["files_loaded"].append(filename)
        if doc_type not in stats["doc_types"]:
            stats["doc_types"][doc_type] = {"files": 0, "chunks": 0}
        stats["doc_types"][doc_type]["files"] += 1
        stats["doc_types"][doc_type]["chunks"] += len(chunks)
    
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    stats["total_chunks"] = chunk_counter
    
    return stats
