import litellm
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable

class BaseAgent(ABC):
    """
    An abstract base class that defines the basic structure and functionality for an agent.
    This version supports multi-step tool calls and has refined error handling without console output.
    """
    def __init__(
        self,
        model: str = "gemini/gemini-2.5-flash", # specify model gemini/gemini-2.5-flash, ollama/llama3:8b for example
        temperature: float = 0.1,
        max_tokens: int = 4096,
        timeout: int = 300,
        max_tool_calls: int = 5
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_tool_calls = max_tool_calls

    @abstractmethod
    def _get_system_message(self) -> str:
        pass

    @abstractmethod
    def _get_tools(self) -> List[Dict[str, Any]]:
        pass
        
    @abstractmethod
    def _get_tool_functions(self) -> Dict[str, Callable]:
        pass

    def _execute_tool_call(self, tool_call) -> Dict[str, Any]:
        function_name = tool_call.function.name
        
        try:
            function_args = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError as e:
            return {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": f"Error: Invalid arguments received from model. Not valid JSON. Details: {e}",
            }
        
        available_tools = self._get_tool_functions()
        
        if function_name not in available_tools:
            return {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": f"Error: Unknown tool '{function_name}' was called by the model.",
            }
        
        function_to_call = available_tools[function_name]
        try:
            result = function_to_call(**function_args)
            return {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": str(result),
            }
        except Exception as e:
            return {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": f"Error while executing tool '{function_name}': {e}",
            }

    def execute_task(self, user_message: str) -> str:
        messages = [
            {"role": "system", "content": self._get_system_message()},
            {"role": "user", "content": user_message}
        ]
        
        for _ in range(self.max_tool_calls):

            # Get the list of tools from the specific agent implementation.
            tools = self._get_tools()
            # Prepare the arguments for the litellm.completion call.
            completion_kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "timeout": self.timeout
            }
            # Only add tool-related parameters if the agent actually has tools.
            if tools:
                completion_kwargs["tools"] = tools
                completion_kwargs["tool_choice"] = "auto"

            try:
                # Use dictionary unpacking to pass the conditional arguments.
                response = litellm.completion(**completion_kwargs)
            except Exception as e:
                return f"Error: Failed to get a response from the model. Details: {e}"
            
            if not response.choices or not response.choices[0].message:
                 return "Error: Received an invalid or empty response from the model."

            response_message = response.choices[0].message
            messages.append(response_message)

            if not response_message.tool_calls:
                return response_message.content or "Task finished, but no final text content was provided."

            tool_outputs = []
            for tool_call in response_message.tool_calls:
                tool_result = self._execute_tool_call(tool_call)
                tool_outputs.append(tool_result)
            
            messages.extend(tool_outputs)
            
        return "Error: Agent could not complete the task within the maximum number of tool calls."