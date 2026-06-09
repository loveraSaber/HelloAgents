import sys
sys.path.append(".")
from LLM.HelloAgentsLLM import HelloAgentsLLM
from executor.toolexecutor import ToolExecutor
import re
class ReActAgent:
    def __init__(self,llm_client:HelloAgentsLLM,tool_executor:ToolExecutor,max_steps:int=5):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []
    def read_prompt(file_name: str) -> str:
        with open(f"C:\Users\qq152\Desktop\Agent\Hello_agents\chapter4\template\{file_name}", "r", encoding="utf-8") as f:
            return f.read()
    def run(self,question:str):
        self.history=[]
        current_step=0
        while current_step<self.max_steps:
            current_step+=1
            print(f"\n--- Step {current_step} ---")
            tools_desc=self.tool_executor.getAviableTools()
            history_str="\n".join(self.history)
            prompt=self.read_prompt("ReAct.txt").format(
                tools=tools_desc,
                question=question,
                history=history_str
            )
            messages=[{"role":"system","content":prompt}]
            response_text=self.llm_client.think(messages=messages)
            if not response_text:
                print("LLM未返回任何内容，终止执行。")
                break
            thought,action=self._parse_output(response_text)
            if  thought:
                print(f"💡 Thought: {thought}")
            if not action:
                print("LLM未返回有效的Action，终止执行。")
                break
            if  action.startswith("Finish"):
                finish_answer=re.match(r"Finish\[(.*)\]",action).group(1)
                print(f"✅ Agent完成任务，答案: {finish_answer}")
                return finish_answer
            tool_name,tool_input=self._parse_action(action)
            if not tool_name or not tool_input:
                print("LLM返回的Action格式不正确，无法解析工具名称和输入，终止执行。")
                break
            print(f"🔧 执行工具: {tool_name} 输入: {tool_input}")
            tool_function=self.tool_executor.gettool(tool_name)
            if not tool_function:
                observation=f"错误:未找到名为 '{tool_name}' 的工具。"
            else:
                observation=tool_function(tool_input)
            print(f"👀 观察 (Observation): {observation}")
            self.history.append(f"Thought: {thought}\nAction: {action}\nObservation: {observation}")
        print("⚠️ 达到最大步骤数，终止执行。")
        return None
    def _parse_output(self, text: str):
        """解析LLM的输出，提取Thought和Action。
        """
        # Thought: 匹配到 Action: 或文本末尾
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        # Action: 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action
    def _parse_action(self, action_text: str):
        """解析Action字符串，提取工具名称和输入。
        """
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None