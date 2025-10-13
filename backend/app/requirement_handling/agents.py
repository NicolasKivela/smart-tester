from typing import Dict, Callable
from app.common.base_agent import BaseAgent
from .file_handler import extract_text
from .topic_detection import detect_topics
from .topic_summary import summarize_topic
from .requirement_extractor import extract_requirements
from .save_file import save_to_file

class RequirementAgent(BaseAgent):
    def _get_system_message(self) -> str:
        return (
            "You are an intelligent assistant that analyzes software requirement documents. "
            "You detect topics, summarize them, and extract detailed requirements."
        )

    def _get_tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "detect_topics",
                    "description": "Detect the main topics in a requirement document.",
                    "parameters": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]},
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "summarize_topic",
                    "description": "Summarize the content for a given topic in the document.",
                    "parameters": {"type": "object", "properties": {"text": {"type": "string"}, "topic": {"type": "string"}}, "required": ["text", "topic"]},
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "extract_requirements",
                    "description": "Extract structured requirements for a topic.",
                    "parameters": {"type": "object", "properties": {"text": {"type": "string"}, "topic": {"type": "string"}}, "required": ["text", "topic"]},
                }
            },
        ]

    def _get_tool_functions(self) -> Dict[str, Callable]:
        return {
            "detect_topics": detect_topics,
            "summarize_topic": summarize_topic,
            "extract_requirements": extract_requirements,
        }