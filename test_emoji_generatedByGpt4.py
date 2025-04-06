import pytest
from emoji import analyze
from emoji.tokenizer import Token, EmojiMatch, EmojiMatchZWJNonRGI

def test_analyze_basic_emoji_only():
    result = list(analyze("Hello 👋🌍", non_emoji=False))
    # Only emojis should be returned
    assert all(isinstance(token, Token) for token in result)
    for token in result:
        assert isinstance(token.value, (EmojiMatch, EmojiMatchZWJNonRGI))
        assert token.chars in ["👋", "🌍"]

def test_analyze_with_non_emoji():
    result = list(analyze("Hi 😄!", non_emoji=True))
    expected = ["H", "i", " ", "😄", "!"]
    output_chars = [token.chars for token in result]
    assert output_chars == expected
    for token in result:
        assert isinstance(token, Token)
        assert isinstance(token.value, (str, EmojiMatch, EmojiMatchZWJNonRGI))

def test_analyze_with_zwj_joined_emoji():
    # 👨‍👩‍👧‍👦 is a family emoji made with ZWJs
    text = "👨‍👩‍👧‍👦 is a family"
    result = list(analyze(text, non_emoji=True, join_emoji=True))
    joined_emoji = result[0]
    assert joined_emoji.chars == "👨‍👩‍👧‍👦"
    assert isinstance(joined_emoji.value, EmojiMatchZWJNonRGI)

def test_analyze_zwj_split():
    # If join_emoji is False, ZWJ emojis should be split
    text = "👨‍👩‍👧‍👦"
    result = list(analyze(text, non_emoji=False, join_emoji=False))
    # We expect multiple EmojiMatch objects instead of a single ZWJ emoji
    assert any(isinstance(token.value, EmojiMatch) for token in result)
    assert not any(isinstance(token.value, EmojiMatchZWJNonRGI) for token in result)

def test_analyze_edge_empty_string():
    result = list(analyze("", non_emoji=True))
    assert result == []

def test_analyze_only_text():
    result = list(analyze("Just text, no emoji!", non_emoji=True))
    output_chars = [token.chars for token in result]
    assert output_chars == list("Just text, no emoji!")
    assert all(isinstance(token.value, str) for token in result)

def test_analyze_mixed_text_and_emoji():
    text = "Pizza 🍕 is life 😍"
    result = list(analyze(text, non_emoji=True))
    output_chars = [token.chars for token in result]
    assert "🍕" in output_chars and "😍" in output_chars
    assert all(isinstance(token, Token) for token in result)
