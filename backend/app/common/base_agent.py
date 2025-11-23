import litellm
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable
from app.common.logs.logger_config import logger
from app.common.token_logging.service import TokenLoggerService, SESSION_TOKEN_LOGGERS
import asyncio
import inspect

class BaseAgent(ABC):
    """
    An abstract base class that provides a structured template for creating LLM-powered agents.

    This class handles the core logic of communicating with a language model, including
    multi-step tool calls. To create a new agent, you must inherit from this class
    and implement the three abstract methods:
    1. _get_system_message()
    2. _get_tools()
    3. _get_tool_functions()
    
    Detailed instructions and examples are provided in the docstring of each abstract method.
    """
    def __init__(
        self,
        session_id: str,
        agent: str,
        model: str = "gemini/gemini-2.5-flash-lite",# specify model gemini/gemini-2.5-flash, ollama/llama3:8b,moonshot/kimi-k2-0905-preview",# specify m for example
        temperature: float = 0.1,
        max_tokens: int = 10000,
        timeout: int = 3000,
        max_tool_calls: int = 5,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_tool_calls = max_tool_calls
        self.agent = agent
        
        # Initialize token logger ONCE per session
        if session_id not in SESSION_TOKEN_LOGGERS:
            SESSION_TOKEN_LOGGERS[session_id] = TokenLoggerService(session_id)

        self.token_logger = SESSION_TOKEN_LOGGERS[session_id]
        self.session_id = session_id
        self.api_call_counter = 0



    @abstractmethod
    def _get_system_message(self) -> str:
        """
        **Implement this method to define the agent's persona and instructions.**

        The system message sets the context for the language model. It should define
        the agent's role, personality, capabilities, and any constraints or rules
        it must follow.

        Returns:
            A string containing the system message.

        ---
        **Example Implementation:**
        ---
        ```python
        def _get_system_message(self) -> str:
            return (
                "You are a helpful assistant who is an expert in Finnish history. "
                "Be polite, engaging, and provide detailed answers."
            )
        ```
        """
        pass

    @abstractmethod
    def _get_tools(self) -> List[Dict[str, Any]]:
        """
        **Implement this method to declare the tools the agent can use.**

        This method must return a list of dictionaries, where each dictionary defines
        a tool according to the OpenAI/LiteLLM function-calling schema. This declaration
        allows the LLM to know what functions are available, what they do, and what
        parameters they accept.

        If the agent does not use any tools, return an empty list `[]`.

        Returns:
            A list of tool definition dictionaries.

        ---
        **Example Implementation (for a weather tool):**
        ---
        ```python
        def _get_tools(self) -> List[Dict[str, Any]]:
            return [
                {
                    "type": "function",
                    "function": {
                        "name": "get_current_weather",
                        "description": "Get the current weather for a specified location.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and country, e.g., 'Tampere, Finland'."
                                },
                                "unit": {
                                    "type": "string",
                                    "enum": ["celsius", "fahrenheit"],
                                    "description": "The temperature unit to use."
                                }
                            },
                            "required": ["location"]
                        }
                    }
                }
            ]
        ```
        ---
        **Example Implementation (for an agent with NO tools):**
        ---
        ```python
        def _get_tools(self) -> List[Dict[str, Any]]:
            return []
        ```
        """        
        pass
        
    @abstractmethod
    def _get_tool_functions(self) -> Dict[str, Callable]:
        """
        **Implement this method to map tool names to the actual Python functions.**

        The BaseAgent's execution logic uses this dictionary to find and execute the
        correct Python function when the LLM requests a tool call. The keys in the
        dictionary must exactly match the 'name' of the functions defined in `_get_tools`.

        If the agent does not use any tools, return an empty dictionary `{}`.

        Returns:
            A dictionary mapping tool names (str) to callable functions.
        
        ---
        **Example Implementation (matching the weather tool):**
        ---
        ```python
        # It's good practice to define your tool functions in a separate file
        # from my_app.tools import get_current_weather

        def _get_tool_functions(self) -> Dict[str, Callable]:
            return {
                "get_current_weather": get_current_weather
            }
        ```
        ---
        **Example Implementation (for an agent with NO tools):**
        ---
        ```python
        def _get_tool_functions(self) -> Dict[str, Callable]:
            return {}
        ```
        """        
        pass

    async def _aexecute_tool_call(self, tool_call) -> Dict[str, Any]:
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
            if inspect.iscoroutinefunction(function_to_call):
                result = await function_to_call(**function_args)
            else:
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

    async def execute_task(self, user_message: str, response_format=None) -> str:
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
                "timeout": self.timeout,
                "response_format": response_format #Output format as a parameter from sub agents
            }
            # Only add tool-related parameters if the agent actually has tools.
            if tools:
                completion_kwargs["tools"] = tools
                completion_kwargs["tool_choice"] = "auto"

            try:
                # Logging input
                logger.info("LITELLM INPUT")
                print(completion_kwargs)
                logger.info(json.dumps(completion_kwargs, indent=2, ensure_ascii=False))

                response = await litellm.acompletion(**completion_kwargs)
                self.api_call_counter += 1
                
                print("API calls made",self.api_call_counter)

                # Logging output
                logger.info("LITELLM RESPONSE")
                try:
                    # If response on LLMResponse-object is turned into JSON
                    logger.info(json.dumps(response.dict(), indent=2, ensure_ascii=False))

                except Exception:
                    logger.info(str(response))

                # log token usage
                usage = getattr(response, "usage", None)
                if usage:
                    print("entry loading")
                    entry = self.token_logger.log_api_call(usage, completion_kwargs, agent=self.agent)
                    print("Entry",entry)
                    logger.info(f"TOKENS USED: {entry}")

                logger.info(f"API CALL COUNT: {self.api_call_counter}")

            except Exception as e:
                logger.error(f"Error in LLM call: {e}")
                return {"status_code": 400,"detail":f"Error: Failed to get a response from the model. Details: {e}"}
            
            if not response.choices or not response.choices[0].message:
                 return "Error: Received an invalid or empty response from the model."

            response_message = response.choices[0].message
            messages.append(response_message)

            if not response_message.tool_calls:
                return response_message.content or "Task finished, but no final text content was provided."

            tool_outputs = await asyncio.gather(
                *(self._aexecute_tool_call(tool_call) for tool_call in response_message.tool_calls)
            )
            
            messages.extend(tool_outputs)

        return "Error: Agent could not complete the task within the maximum number of tool calls."
    

