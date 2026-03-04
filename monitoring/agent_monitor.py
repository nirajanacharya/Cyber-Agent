"""Monitored agent wrapper with Logfire."""

from datetime import datetime
import logfire
from .session_tracker import SessionTracker
from .cost_calculator import estimate_tokens, estimate_cost


class MonitoredAgent:
    """Wrap agent with monitoring capabilities."""
    
    def __init__(self, agent, session_tracker: SessionTracker = None):
        self.agent = agent
        self.tracker = session_tracker or SessionTracker()
    
    async def query(self, user_question: str, session_id: str = None, **kwargs):
        """Query agent with full monitoring."""
        start_time = datetime.now()
        
        
        if session_id:
            self.tracker.track_query(session_id, user_question)
        
        
        with logfire.span(
            "agent_query",
            question=user_question[:100],
            session_id=session_id,
            model=kwargs.get('model', 'gpt-4o-mini')
        ):
            try:
                
                result = await self.agent.query(user_question, **kwargs)
                
               
                duration_ms = (datetime.now() - start_time).total_seconds() * 1000
                tokens = estimate_tokens(user_question, result['answer'])
                cost = estimate_cost(tokens, kwargs.get('model', 'gpt-4o-mini'))
                
              
                logfire.info(
                    "Query completed",
                    duration_ms=round(duration_ms, 2),
                    tokens=tokens,
                    cost=cost,
                    tools=result['tools_used']
                )
                
                
                if session_id:
                    self.tracker.track_response(session_id, tokens, duration_ms)
                
               
                result['monitoring'] = {
                    'duration_ms': duration_ms,
                    'tokens': tokens,
                    'cost': cost,
                    'session_id': session_id
                }
                
                return result
                
            except Exception as e:
                logfire.error("Query failed", error=str(e))
                if session_id:
                    self.tracker.track_error(session_id)
                raise
    
    def get_session_stats(self, session_id: str):
        """Get statistics for a session."""
        return self.tracker.get_stats(session_id)
    
    def clear_history(self):
        """Clear agent conversation history."""
        self.agent.clear_history()
