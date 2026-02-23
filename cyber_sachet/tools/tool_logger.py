"""Tool call logging and statistics tracking."""

from typing import List, Dict, Any
from collections import Counter
from ..models.tool_call import ToolCall


class ToolLogger:
    """Tracks tool calls for debugging and testing."""
    
    def __init__(self, enable_logging: bool = True):
        """Initialize logger."""
        self.enable_logging = enable_logging
        self.tool_call_history: List[ToolCall] = []
    
    def log_call(self, tool_name: str, args: Dict[str, Any], result: Any, duration_ms: float):
        """Log a tool call."""
        if self.enable_logging:
            self.tool_call_history.append(
                ToolCall(
                    tool_name=tool_name,
                    args=args,
                    result=result,
                    duration_ms=duration_ms
                )
            )
    
    def get_history(self) -> List[ToolCall]:
        """Get history of all tool calls."""
        return self.tool_call_history
    
    def clear_history(self):
        """Clear tool call history."""
        self.tool_call_history = []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about tool usage."""
        if not self.tool_call_history:
            return {"total_calls": 0}
        
        tool_counts = Counter([call.tool_name for call in self.tool_call_history])
        avg_duration = sum(call.duration_ms for call in self.tool_call_history) / len(self.tool_call_history)
        
        return {
            "total_calls": len(self.tool_call_history),
            "tool_counts": dict(tool_counts),
            "average_duration_ms": round(avg_duration, 2),
            "total_duration_ms": sum(call.duration_ms for call in self.tool_call_history)
        }
