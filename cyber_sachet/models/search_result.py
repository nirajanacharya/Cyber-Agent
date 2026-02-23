"""Search result data model."""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class SearchResult:
    """Structured search result from vector database."""
    content: str
    source: str
    doc_type: str
    relevance_score: float
    chunk_id: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "content": self.content,
            "source": self.source,
            "doc_type": self.doc_type,
            "relevance_score": self.relevance_score,
            "chunk_id": self.chunk_id,
            "metadata": self.metadata
        }
