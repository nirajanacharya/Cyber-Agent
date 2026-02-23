"""Tool selection logic for the agent."""

from typing import List


def select_tools_for_query(question: str) -> List[str]:
    """
    Select appropriate tools based on query keywords.
    
    Args:
        question: User's question
    
    Returns:
        List of tool names to use
    """
    question_lower = question.lower()
    selected_tools = []
    
   
    if any(word in question_lower for word in ['penalty', 'punishment', 'fine', 'imprisonment', 'sentence']):
        selected_tools.append('check_penalty_tool')
        selected_tools.append('semantic_search_tool')  
    
   
    elif any(word in question_lower for word in ['law', 'act', 'legal', 'regulation', 'statute']):
        selected_tools.append('search_laws_tool')
    
    
    elif any(word in question_lower for word in ['how to', 'how can', 'protect', 'secure', 'safe', 'prevent', 'avoid', 'tips']):
        selected_tools.append('search_awareness_tool')
    
   
    else:
        selected_tools.append('semantic_search_tool')
    
    return selected_tools


def extract_crime_type(question: str) -> str:
    """
    Extract crime type from penalty-related questions.
    
    Args:
        question: User's question
    
    Returns:
        Crime type string
    """
    question_lower = question.lower()
    
    
    crime_types = {
        'hack': 'hacking',
        'hacking': 'hacking',
        'fraud': 'fraud',
        'phishing': 'phishing',
        'theft': 'theft',
        'steal': 'theft',
        'breach': 'breach',
        'access': 'unauthorized access',
        'unauthorized': 'unauthorized access',
        'malware': 'malware',
        'virus': 'malware',
        'ransomware': 'ransomware',
        'identity': 'identity theft',
        'spam': 'spam',
        'cyberbully': 'cyberbullying',
        'harassment': 'harassment'
    }
    
    
    for keyword, crime_type in crime_types.items():
        if keyword in question_lower:
            return crime_type
    
    
    return 'cybercrime'
