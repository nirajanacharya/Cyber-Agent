"""Document sources retrieval tool."""

import asyncio
from typing import Dict, Any


async def get_document_sources_tool(collection) -> Dict[str, Any]:
    """
    Get list of all indexed document sources with statistics.
    
    Provides metadata about what documents are available in the
    knowledge base and how many chunks each has been split into.
    
    Args:
        collection: ChromaDB collection
    
    Returns:
        Dictionary with:
            - total_documents: Number of unique documents
            - total_chunks: Total number of text chunks
            - sources: Dict mapping filename to metadata
    """
    all_data = await asyncio.to_thread(collection.get)
    
    sources = {}
    for meta in all_data['metadatas']:
        source = meta['source']
        doc_type = meta['doc_type']
        
        if source not in sources:
            sources[source] = {
                "type": doc_type,
                "chunks": 0
            }
        sources[source]["chunks"] += 1
    
    return {
        "total_documents": len(sources),
        "total_chunks": len(all_data['metadatas']),
        "sources": sources
    }
