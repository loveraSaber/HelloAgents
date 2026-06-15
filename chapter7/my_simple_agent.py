from typing import Optional,Iterator
from hello_agents import SimpleAgent,HelloAgentsLLM,Config,Message
class MySimpleAgent(SimpleAgent):
    def __init__(
            self,
            name:str,
            llm:HelloAgentsLLM,
            system_prompt:Optional[str]=None,
            config:Optional[Config]=None,
            tool_registry:Optional['ToolRegistry']=None,
            enable_tool_calling:bool=True
    ):
        super().__init__(name,llm,system_prompt,config)
        self.tool_registry=tool_registry
        self.enable_tool_calling=enable_tool_calling and tool_registry is not None
        print(f"✅ {name} 初始化完成，工具调用: {'启用' if self.enable_tool_calling else '禁用'}")
    
    def run(self,input_text:str,max_tool_iterations:int=3,**kwargs)->str:
        print(f"🤖{self.name}正在处理：{input_text}")
        message=[]
        enhanced_system_prompt=self._get_en
    def _get_enhanced_system_prompt(self)->str:
        base_prompt=self.sys_prompt or "你是一个有用的AI助手"
        if not self.enable_tool_calling or not self.tool_registry:
            return base_prompt
        tool_description=self.tool_registry.get_tools_description()
        if not tool_description or tool_description=="暂无可用工具":
            return base_prompt
        tools_section = "\n\n## 可用工具\n"
        tools_section += "你可以使用以下工具来帮助回答问题:\n"
        tools_section += tool_description + "\n"

        tools_section += "\n## 工具调用格式\n"
        tools_section += "当需要使用工具时，请使用以下格式:\n"
        tools_section += "`[TOOL_CALL:{tool_name}:{parameters}]`\n"
        tools_section += "例如:`[TOOL_CALL:search:Python编程]` 或 `[TOOL_CALL:memory:recall=用户信息]`\n\n"
        tools_section += "工具调用结果会自动插入到对话中，然后你可以基于结果继续回答。\n"
        return base_prompt+tools_section
    