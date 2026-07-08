"""
LLM Service - Handles OpenAI API interactions (Updated for OpenAI v1.0+)
"""
from openai import OpenAI
from typing import List, Dict, Optional, Any
from config.settings import Config
from utils.logger import logger
from tools import TOOLS
from tools.suggestion_tools import SUGGESTION_TOOL

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.LLM_MODEL
        self.temperature = Config.LLM_TEMPERATURE
        self.max_tokens = Config.LLM_MAX_TOKENS
        self.all_tools = TOOLS + [SUGGESTION_TOOL]
        logger.info(f"LLM Service initialized with model: {self.model}")
        logger.info(f"Loaded {len(self.all_tools)} tools")
    
    def generate_response(self, 
                         messages: List[Dict[str, str]], 
                         system_prompt: str,
                         tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
        try:
            full_messages = [
                {"role": "system", "content": system_prompt}
            ] + messages
            tools_to_use = tools if tools is not None else self.all_tools
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                tools=tools_to_use,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            # Convert to dict for compatibility
            message_dict = {
                "role": message.role,
                "content": message.content
            }
            if hasattr(message, 'tool_calls') and message.tool_calls:
                message_dict["tool_calls"] = [
                    {
                        "id": tc.id,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
                logger.info(f"LLM requested {len(message.tool_calls)} tool call(s)")
            else:
                logger.info(f"LLM generated: {message.content[:50] if message.content else '...'}...")
            return message_dict
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {"content": f"I encountered an error: {str(e)}"}
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        try:
            from tools import add_study_task, list_study_tasks, complete_study_task, delete_study_task
            from tools.suggestion_tools import suggest_topic
            tool_map = {
                "add_study_task": add_study_task,
                "list_study_tasks": list_study_tasks,
                "complete_study_task": complete_study_task,
                "delete_study_task": delete_study_task,
                "suggest_topic": suggest_topic
            }
            if tool_name not in tool_map:
                return f"Error: Tool '{tool_name}' not found"
            result = tool_map[tool_name](**arguments)
            logger.info(f"Executed tool '{tool_name}' with arguments: {arguments}")
            return result
        except Exception as e:
            logger.error(f"Error executing tool '{tool_name}': {e}")
            return f"Error executing tool: {str(e)}"
    
    def process_with_tools(self, 
                          messages: List[Dict[str, str]], 
                          system_prompt: str) -> Dict[str, Any]:
        response = self.generate_response(messages, system_prompt)
        if response.get("tool_calls"):
            tool_results = []
            for tool_call in response["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                # Safely evaluate arguments
                try:
                    import json
                    arguments = json.loads(tool_call["function"]["arguments"])
                except:
                    arguments = {}
                result = self.execute_tool(tool_name, arguments)
                tool_results.append({
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "name": tool_name,
                    "content": result
                })
            messages.append(response)
            messages.extend(tool_results)
            final_response = self.generate_response(messages, system_prompt, tools=[])
            return final_response
        return response
