"""System prompts for the agent."""

import re


def detect_response_language(user_question: str) -> str:
    """Detect desired response language from user input.

    Returns:
        "nepali" when Devanagari Unicode text or likely Romanized Nepali
        is detected, otherwise "english".
    """
    for char in user_question:
        code_point = ord(char)
        if 0x0900 <= code_point <= 0x097F:
            return "nepali"

 
    romanized_markers = {
        "malai", "ma", "mero", "hamro", "tapai", "tapaiko", "timilai",
        "timro", "hajur", "kasari", "kina", "k", "ke", "yo", "tyo",
        "ho", "cha", "chha", "xa", "bhayo", "gareko", "garyo", "garna",
        "sakchu", "sakdina", "sahayog", "samasya", "bujhina", "nepal",
        "kanun", "surakshya", "suraksha", "harras", "harass", "garayo",
    }
    tokens = re.findall(r"[a-zA-Z]+", user_question.lower())
    marker_count = sum(1 for token in tokens if token in romanized_markers)
    if marker_count >= 2:
        return "nepali"

    return "english"

SYSTEM_PROMPT = """You are Cyber Sachet, an AI assistant specializing in cyber security awareness 
and Nepal's cyber laws (IT Act 2063, Digital Security Act 2024).

Your mission:
1. Provide accurate, helpful information about cyber security
2. Explain Nepal's cyber laws in clear, accessible language
3. Offer practical security advice and best practices
4. ALWAYS cite sources when referencing specific laws or regulations
5. Be educational, empathetic, and solution-oriented

When answering questions:
- Synthesize information from the provided context documents
- Provide actionable, practical advice
- Cite the specific document source for legal information using format: [Source: filename]
- Use clear, simple language that non-technical users can understand
- If the context doesn't contain the answer, clearly state that and use your general knowledge
- For cyber security tips, prioritize practical, implementable advice
- When discussing laws, always mention the specific act name (e.g., "Nepal IT Act 2063")

Format your responses:
- Use clear structure with headings when appropriate
- Use bullet points for lists
- Always include source citations for legal information in format [Source: filename]
- Keep language accessible and jargon-free

Remember: Your goal is to educate and empower users about cyber security and their legal rights/responsibilities in Nepal."""


def get_user_message(context: str, user_question: str) -> str:
    """
    Build user message with context and question.
    
    Args:
        context: Document context
        user_question: User's question
    
    Returns:
        Formatted user message with response language instruction
    """
    response_language = detect_response_language(user_question)
    language_instruction = (
        "Respond fully in Nepali (Devanagari script)."
        if response_language == "nepali"
        else "Respond fully in English."
    )

    return f"""Based on the following context from cyber security documents and Nepal's cyber laws, 
please answer the user's question comprehensively.

RESPONSE LANGUAGE REQUIREMENT:
{language_instruction}

CONTEXT DOCUMENTS:
{context}

USER QUESTION: {user_question}

Provide a comprehensive, well-structured answer. IMPORTANT: When referencing specific laws or regulations, 
cite the source document in the format [Source: filename]. Make your answer practical and actionable."""
