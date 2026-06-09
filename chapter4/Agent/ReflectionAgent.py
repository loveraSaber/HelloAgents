import os
import sys
sys.path.append(".")
from Memory.ShortMemory import ShortMemory
from LLM.HelloAgentsLLM import HelloAgentsLLM
class ReflectionAgent:
    def __init__(self,llm_client,max_iterations=3):
        self.llm_client=llm_client
        self.memory=ShortMemory()
        self.max_iterations=max_iterations
    def read_prompt(self,file_name:str)->str:
        template_dir = os.path.join(os.path.dirname(__file__), "..", "template")
        file_path = os.path.join(template_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    def run(self,task:str):
        print(f"🔍 任务: {task}")
        print("🚀 开始执行任务...")
        initial_prompt=self.read_prompt("Execution.txt").format(
            task=task
        )
        initial_code=self.llm_client.think(messages=[{"role":"system","content":initial_prompt}]) or ""
        print(f"💡 初始执行结果:\n{initial_code}")
        self.memory.add_record(task,initial_code)
        for iteration in range(self.max_iterations):
            print(f"开始第{iteration+1}次反思...")
            print("🔍 正在反思...")
            last_code=self.memory.get_last_execution()
            reflection_prompt=self.read_prompt("reflection.txt").format(task=task,code=last_code)
            feedback=self._get_llm_response(reflection_prompt)
            self.memory.add_record("reflection",feedback)
            if "无需改进" in feedback:
                print("✅ 反思结果表明无需改进，任务完成。")
                break
            print("正在优化")
            refine_prompt=self.read_prompt("refinement.txt").format(task=task,last_code_attempt=last_code,feedback=feedback)
            refined_code=self._get_llm_response(refine_prompt)
            self.memory.add_record("execution",refined_code)
        final_code=self.memory.get_last_execution()
        print(f"🎯 最终执行结果:\n{final_code}")
        return final_code
    def _get_llm_response(self,prompt:str)->str:
        messages=[{"role":"system","content":prompt}]
        response=self.llm_client.think(messages=messages) or ""
        return response