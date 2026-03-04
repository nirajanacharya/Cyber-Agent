"""Text formatting utilities."""


def format_duration(ms: float) -> str:
    """Format duration in milliseconds to readable string."""
    if ms < 1000:
        return f"{ms:.0f}ms"
    return f"{ms/1000:.1f}s"


def format_cost(cost: float) -> str:
    """Format cost to readable string."""
    return f"${cost:.6f}"


def format_tokens(tokens: int) -> str:
    """Format token count to readable string."""
    if tokens < 1000:
        return str(tokens)
    return f"{tokens/1000:.1f}k"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
