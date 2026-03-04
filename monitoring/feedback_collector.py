"""Collect user feedback on responses."""

from datetime import datetime
import logfire


class FeedbackCollector:
    """Track user feedback and ratings."""
    
    def __init__(self):
        self.feedback = []
    
    def add_rating(self, session_id: str, query_id: str, rating: str, comment: str = None):
        """Record user rating (positive/negative)."""
        feedback_entry = {
            'session_id': session_id,
            'query_id': query_id,
            'rating': rating,
            'comment': comment,
            'timestamp': datetime.now().isoformat()
        }
        
        self.feedback.append(feedback_entry)
        
        logfire.info("Feedback recorded", **feedback_entry)
    
    def get_summary(self):
        """Get feedback statistics."""
        if not self.feedback:
            return {'total': 0, 'positive': 0, 'negative': 0}
        
        total = len(self.feedback)
        positive = sum(1 for f in self.feedback if f['rating'] == 'positive')
        negative = sum(1 for f in self.feedback if f['rating'] == 'negative')
        
        return {
            'total': total,
            'positive': positive,
            'negative': negative,
            'positive_rate': round(positive / total * 100, 1) if total > 0 else 0
        }
