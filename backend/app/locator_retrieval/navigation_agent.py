import json
from typing import List, Dict, Any, Callable
from app.common.base_agent import BaseAgent
from .page_navigator import PageNavigator
import litellm
import asyncio

class NavigationAgent(BaseAgent):
    """
    An agent that can navigate web pages to accomplish a task.
    """
    def __init__(self, page_navigator: PageNavigator, **kwargs):
        super().__init__(**kwargs)
        self.page_navigator = page_navigator
        self.task_finished = False

    def _get_system_message(self) -> str:
        return """
You are an expert web automation assistant. Your goal is to navigate a website to complete a specific task given by the user.

1.  **Analyze the Task**: Understand the user's goal.
2.  **Inspect the Page**: Use the `get_page_content` tool to see the current state of the web page, including the URL and interactive elements. This is your primary way of seeing the page.
3.  **Formulate a Plan**: Based on the page content and the task, decide which single element to interact with next.
4.  **Execute Action**: Use the `click` or `fill` tools to interact with the chosen element. Use robust CSS selectors to identify elements. You can use the selector suggestions from `get_page_content`.
5.  **Verify and Repeat**: After each action, the page content will change. Use `get_page_content` again to see the result of your action and decide the next step.
6.  **Finish**: When the task is fully accomplished, call the `finish_task` tool with a summary of what you did.

- Always start by navigating to the initial URL if provided, or by using `get_page_content` to understand the current page.
- Be methodical. One step at a time. Inspect, act, inspect, act.
"""

    def _get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "navigate",
                    "description": "Navigates to a specific URL. Should be the first step.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "description": "The URL to navigate to."}
                        },
                        "required": ["url"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "click",
                    "description": "Clicks an element on the page based on a CSS selector.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "selector": {"type": "string", "description": "A robust CSS selector for the element to click."},
                            "description": {"type": "string", "description": "A brief explanation of what is being clicked and why it helps achieve the task."},
                        },
                        "required": ["selector", "description"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "fill",
                    "description": "Fills an input field on the page.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "selector": {"type": "string", "description": "A CSS selector for the input element."},
                            "text": {"type": "string", "description": "The text to fill into the input."},
                            "description": {"type": "string", "description": "A brief explanation of what is being filled and why."},
                        },
                        "required": ["selector", "text", "description"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_page_content",
                    "description": "Returns a summary of the current page, including URL and a list of interactive elements with selector suggestions.",
                    "parameters": {"type": "object", "properties": {}},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "finish_task",
                    "description": "Call this function ONLY when the task is successfully and fully completed.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "summary": {"type": "string", "description": "A concise summary of how the task was completed."}
                        },
                        "required": ["summary"],
                    },
                },
            },
        ]

    def _get_tool_functions(self) -> Dict[str, Callable]:
        return {
            "navigate": self.page_navigator.navigate,
            "click": self.page_navigator.click,
            "fill": self.page_navigator.fill,
            "get_page_content": self.page_navigator.get_page_content,
            "finish_task": self.finish_task,
        }

    def finish_task(self, summary: str) -> str:
        """A tool function to be called when the agent completes the task."""
        self.task_finished = True
        return f"Task finished successfully. Summary: {summary}"

    async def execute_task(self, user_message: str) -> str:
        # Override execute_task to handle the 'finish_task' call and stop the loop.
        messages = [
            {"role": "system", "content": self._get_system_message()},
            {"role": "user", "content": user_message}
        ]
        
        for i in range(self.max_tool_calls):
            if self.task_finished:
                break

            print(f"\n--- Agent Loop {i+1}/{self.max_tool_calls} ---")

            tools = self._get_tools()
            completion_kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "timeout": self.timeout,
                "tools": tools,
                "tool_choice": "auto",
            }

            try:
                response = await litellm.acompletion(**completion_kwargs)
            except Exception as e:
                return f"Error: Failed to get a response from the model. Details: {e}"
            
            response_message = response.choices[0].message
            messages.append(response_message)

            if not response_message.tool_calls:
                final_content = response_message.content or "Task finished without calling finish_task."
                print(f"Agent finished with message: {final_content}")
                return final_content

            tool_outputs = await asyncio.gather(
                *(self._aexecute_tool_call(tool_call) for tool_call in response_message.tool_calls)
            )
            
            messages.extend(tool_outputs)
            
        if not self.task_finished:
            return "Error: Agent could not complete the task within the maximum number of tool calls."
        
        # Find the summary from the last tool call
        final_message = messages[-1]
        if "Task finished successfully" in final_message.get("content", ""):
            return final_message["content"]
        else:
            # This is a fallback, the summary should be in the last message.
            for msg in reversed(messages):
                if msg.get("role") == "tool" and "Task finished successfully" in msg.get("content", ""):
                    return msg["content"]
            return "Task completed, but summary was not found."
