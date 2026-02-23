"""LLM response generation."""

from typing import Dict, Any
from openai import AsyncOpenAI


async def generate_response(
    client: AsyncOpenAI,
    system_prompt: str,
    user_message: str,
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
    verbose: bool = True
) -> str:
    """
    Generate response using OpenAI LLM.
    
    Args:
        client: AsyncOpenAI client
        system_prompt: System prompt
        user_message: User message with context
        model: Model name
        temperature: Temperature setting
        verbose: Print progress
    
    Returns:
        Generated answer string
    """
    if verbose:
        print("Generating response...\n")
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=1500
    )
    
    return response.choices[0].message.content
