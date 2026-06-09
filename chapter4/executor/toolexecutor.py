from typing import Dict,Any
class ToolExecutor:
    def __init__(self):
        self.tools:Dict[str,Dict[str,Any]] = {}
    def register_tool(self,tool_name:str,tool_func:callable,tool_desc:str):
        if tool_name in self.tools:
            raise ValueError(f"Tool {tool_name} already exists.overwrite it.")
        self.tools[tool_name] = {
            "func":tool_func,
            "desc":tool_desc
        }
    def gettool(self,tool_name:str):
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found.")
        return self.tools[tool_name]["func"]
    def getAviableTools(self):
        return "\n".join([
            f"{tool_name}: {tool_info['desc']}" for tool_name,tool_info in self.tools.items()
        ])