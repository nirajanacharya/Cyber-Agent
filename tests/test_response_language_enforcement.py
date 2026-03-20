"""Tests for response language enforcement helpers."""

from cyber_sachet.agent.response_generator import _needs_language_correction


def test_nepali_requires_devanagari_when_missing():
    """Nepali mode should request correction for Latin-only content."""
    assert _needs_language_correction("This is an English answer.", "nepali") is True


def test_nepali_accepts_devanagari_content():
    """Nepali mode should not request correction when Devanagari exists."""
    assert _needs_language_correction("यो नेपाली उत्तर हो।", "nepali") is False


def test_english_accepts_english_content():
    """English mode should not request correction for English content."""
    assert _needs_language_correction("This is an English answer.", "english") is False
