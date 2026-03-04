"""Cost calculation utilities."""


def estimate_tokens(question: str, answer: str) -> int:
    """Estimate tokens from text (rough)."""
   
    chars = len(question) + len(answer)
    return int((chars / 4) * 2.5)


def estimate_cost(tokens: int, model: str = "gpt-4o-mini") -> float:
    """Calculate cost from tokens."""
    pricing = {
        "gpt-4o-mini": {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000},
        "gpt-4o": {"input": 2.50 / 1_000_000, "output": 10.00 / 1_000_000}
    }
    
    rates = pricing.get(model, pricing["gpt-4o-mini"])
    
    
    input_tokens = int(tokens * 0.7)
    output_tokens = int(tokens * 0.3)
    
    cost = (input_tokens * rates["input"]) + (output_tokens * rates["output"])
    return round(cost, 6)
