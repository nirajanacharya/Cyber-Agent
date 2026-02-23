"""Tool call tracking data model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any


@dataclass
class ToolCall:
    """Record of a tool invocation for debugging and testing."""
    tool_name: str
    args: Dict[str, Any]
    result: Any
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    duration_ms: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "tool_name": self.tool_name,
            "args": self.args,
            "timestamp": self.timestamp,
            "duration_ms": self.duration_ms,
            "result_summary": str(self.result)[:200] if self.result else None
        }
