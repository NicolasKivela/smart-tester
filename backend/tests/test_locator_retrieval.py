import pytest
from unittest.mock import patch
from app.locator_retrieval.agents.navigator_agent import NavigatorAgent

def test_construct_prompt_basic():
    """Test the basic prompt construction with task, history, and locators."""
    agent = NavigatorAgent()
    task = "Test task"
    history = ["Step 1", "Step 2"]
    locators = {"locator1": "css_selector"}

    prompt = agent.construct_prompt(task=task, history=history, locators=locators)

    assert "Overall Task: Test task" in prompt
    assert "Action History (what has been done so far):" in prompt
    assert "['Step 1', 'Step 2']" in prompt
    assert "Locators found on the CURRENT page:" in prompt
    assert "{'locator1': 'css_selector'}" in prompt
    assert "Aria Snapshot" not in prompt
    assert not isinstance(prompt, list)

def test_construct_prompt_with_aria_snapshot():
    """Test the prompt construction when aria_snapshot is provided."""
    agent = NavigatorAgent()
    agent.use_aria_snapshot = True
    task = "Test task"
    history = []
    locators = {}
    aria_snapshot = "Aria snapshot data"

    prompt = agent.construct_prompt(task=task, history=history, locators=locators, aria_snapshot=aria_snapshot)

    assert "Aria Snapshot (Accessibility Tree):" in prompt
    assert "Aria snapshot data" in prompt

@patch('app.locator_retrieval.agents.navigator_agent.AgentConfig.NavigatorAgent.use_aria_snapshot', False)
def test_construct_prompt_without_aria_snapshot_when_disabled():
    """Test that the aria_snapshot is not included when use_aria_snapshot is False."""
    agent = NavigatorAgent()
    task = "Test task"
    history = []
    locators = {}
    aria_snapshot = "Aria snapshot data"

    prompt = agent.construct_prompt(task=task, history=history, locators=locators, aria_snapshot=aria_snapshot)

    assert "Aria Snapshot" not in prompt

def test_construct_prompt_with_screenshot():
    """Test the prompt construction when a screenshot is provided and enabled."""
    agent = NavigatorAgent()
    agent.use_screenshot = True
    task = "Test task"
    history = []
    locators = {}
    screenshot = "base64_screenshot_data"

    prompt = agent.construct_prompt(task=task, history=history, locators=locators, screenshot=screenshot)

    assert isinstance(prompt, list)
    assert len(prompt) == 2
    assert prompt[0]['type'] == 'text'
    assert prompt[1]['type'] == 'image_url'
    assert "data:image/jpeg;base64,base64_screenshot_data" in prompt[1]['image_url']['url']

@patch('app.locator_retrieval.agents.navigator_agent.AgentConfig.NavigatorAgent.use_screenshot', False)
def test_construct_prompt_without_screenshot_when_disabled():
    """Test that the screenshot is not included when use_screenshot is False."""
    agent = NavigatorAgent()
    task = "Test task"
    history = []
    locators = {}
    screenshot = "base64_screenshot_data"

    prompt = agent.construct_prompt(task=task, history=history, locators=locators, screenshot=screenshot)

    assert isinstance(prompt, str)
    assert "image_url" not in prompt

