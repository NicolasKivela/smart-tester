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

@pytest.mark.asyncio
async def test_process_req_document_extracts_topics():
    with patch("app.requirement_handling.service.RequirementAgent") as MockAgent:
        mock_agent = MockAgent.return_value
        mock_agent.detect_topics = AsyncMock(return_value=["Login", "Checkout"])

        processor = RequirementsProcessor(
            url="test",
            credentials_input=UrlCredentials(),
            text="Some requirement text",
            req_file="req.txt",
            session_id="123"
        )

        result = await processor.process_req_document()

        assert result == ["Login", "Checkout"]
        assert processor.topics == ["Login", "Checkout"]

@pytest.mark.asyncio
async def test_detect_topics_parses_json():
    agent = RequirementAgent(session_id="1")
    agent.execute_task = AsyncMock(return_value='["Login", "Payment"]')

    result = await agent.detect_topics("text")
    assert result == ["Login", "Payment"]

@pytest.mark.asyncio
async def test_process_req_document_handles_no_topics():
    with patch("app.requirement_handling.service.RequirementAgent") as MockAgent:
        mock_agent = MockAgent.return_value
        mock_agent.detect_topics = AsyncMock(return_value=[])

        processor = RequirementsProcessor(
            url="test",
            credentials_input=UrlCredentials(),
            text="text fore requirements",
            req_file="req.txt",
            session_id="123"
        )

        result = await processor.process_req_document()

        assert result == []
        assert processor.topics == []
