"""Track user sessions and interactions."""

from collections import defaultdict
from datetime import datetime


class SessionTracker:
    """Track session metrics and queries."""
    
    def __init__(self):
        self.sessions = defaultdict(lambda: {
            'queries': [],
            'tokens': 0,
            'duration_ms': 0,
            'errors': 0,
            'created': datetime.now().isoformat()
        })
    
    def track_query(self, session_id: str, query: str):
        """Add query to session."""
        self.sessions[session_id]['queries'].append({
            'text': query,
            'timestamp': datetime.now().isoformat()
        })
    
    def track_response(self, session_id: str, tokens: int, duration_ms: float):
        """Add response metrics."""
        session = self.sessions[session_id]
        session['tokens'] += tokens
        session['duration_ms'] += duration_ms
    
    def track_error(self, session_id: str):
        """Increment error count."""
        self.sessions[session_id]['errors'] += 1
    
    def get_stats(self, session_id: str):
        """Get session statistics."""
        session = self.sessions.get(session_id, {})
        query_count = len(session.get('queries', []))
        
        return {
            'queries': query_count,
            'tokens': session.get('tokens', 0),
            'avg_duration': session.get('duration_ms', 0) / query_count if query_count > 0 else 0,
            'errors': session.get('errors', 0)
        }
