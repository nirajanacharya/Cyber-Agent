"""Language routing tests for response generation prompts."""

from cyber_sachet.agent.prompts import detect_response_language, get_user_message


def test_detect_response_language_devanagari_returns_nepali():
    """Devanagari Unicode input should route response language to Nepali."""
    question = "नेपालमा फिसिङबाट कसरी जोगिने?"
    assert detect_response_language(question) == "nepali"


def test_detect_response_language_english_returns_english():
    """English input should route response language to English."""
    question = "How can I stay safe from phishing attacks?"
    assert detect_response_language(question) == "english"


def test_detect_response_language_romanized_nepali_returns_nepali():
    """Romanized Nepali input should route response language to Nepali."""
    question = "malai euta le harras garyo kasari safe hunchu"
    assert detect_response_language(question) == "nepali"


def test_get_user_message_includes_nepali_instruction_for_devanagari_input():
    """Prompt should include Nepali language requirement when input is Devanagari."""
    message = get_user_message("sample context", "पासवर्ड कत्तिको बलियो हुनुपर्छ?")
    assert "Respond fully in Nepali (Devanagari script)." in message


def test_get_user_message_includes_english_instruction_for_english_input():
    """Prompt should include English language requirement when input is English."""
    message = get_user_message("sample context", "What is two-factor authentication?")
    assert "Respond fully in English." in message


def test_get_user_message_romanized_nepali_includes_nepali_instruction():
    """Romanized Nepali input should still force Nepali response."""
    message = get_user_message("sample context", "malai password kasari secure garne")
    assert "Respond fully in Nepali (Devanagari script)." in message
