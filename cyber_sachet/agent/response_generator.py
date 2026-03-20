"""LLM response generation."""

from typing import Dict, Any
from openai import AsyncOpenAI


def _contains_devanagari(text: str) -> bool:
    """Return True if text contains any Devanagari Unicode characters."""
    return any(0x0900 <= ord(char) <= 0x097F for char in text)


def _needs_language_correction(answer: str, response_language: str) -> bool:
    """Check whether generated answer violates the requested output language."""
    if response_language == "nepali":
        return not _contains_devanagari(answer)
    if response_language == "english":
        return _contains_devanagari(answer)
    return False


async def generate_response(
    client: AsyncOpenAI,
    system_prompt: str,
    user_message: str,
    response_language: str,
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
        response_language: Required output language ("nepali" or "english")
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

    answer = response.choices[0].message.content

    if _needs_language_correction(answer, response_language):
        if verbose:
            print("Enforcing response language...")

        if response_language == "nepali":
            correction_instruction = (
                "Rewrite the answer in natural Nepali using Devanagari script only. "
                "Preserve factual meaning and keep citations like [Source: filename] unchanged."
            )
        else:
            correction_instruction = (
                "Rewrite the answer fully in English. "
                "Preserve factual meaning and keep citations like [Source: filename] unchanged."
            )

        correction_response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": correction_instruction},
                {"role": "user", "content": answer},
            ],
            temperature=0,
            max_tokens=1500,
        )
        answer = correction_response.choices[0].message.content

    return answer
