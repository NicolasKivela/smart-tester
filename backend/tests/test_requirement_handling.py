import pytest
from unittest.mock import AsyncMock, patch

from app.requirement_handling.file_handler import clean_text, extract_text
from app.requirement_handling.service import RequirementsProcessor
from app.requirement_handling.schemas import UrlCredentials
from app.requirement_handling.agents import RequirementAgent

def test_clean_text_removes_extra_spaces():
    input_text = "This   is    a   test"
    expected = "This is a test"
    assert clean_text(input_text) == expected

def test_clean_text_removes_multiple_newlines():
    input_text = "Line1\n\n\nLine2\n\n"
    expected = "Line1\nLine2"
    assert clean_text(input_text) == expected

def test_clean_text_strips_whitespace():
    input_text = "   Hello world   "
    expected = "Hello world"
    assert clean_text(input_text) == expected

def test_clean_text_empty():
    assert clean_text("") == ""

def test_clean_text_only_spaces():
    assert clean_text("      ") == ""
