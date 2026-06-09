import os
from LLM.HelloAgentsLLM import HelloAgentsLLM

class planExecutor:
    def __init__(self, llm_client: HelloAgentsLLM):
        self.llm_client = llm_client

    def read_prompt(self, file_name: str) -> str:
        template_dir = os.path.join(os.path.dirname(__file__), "..", "template")
        file_path = os.path.join(template_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def execute(self, question: str, plan: list[str]) -> str:
        history=[]
        print("🚀 执行计划中...")
        for i,step in enumerate(plan):
            print(f"\n--- 执行步骤 {i+1}/{len(plan)} ---")
            prompt=self.read_prompt("executor.txt").format(
                question=question,
                plan=plan,
                current_step=step,
                history="\n".join(history) if history else "无"
            )
            messages=[{"role":"system","content":prompt}]
            response_text=self.llm_client.think(messages=messages) or ""
            print(f"LLM响应:\n{response_text}")
            history.append(f"Step: {step}\nResponse: {response_text}")
        final_answer=response_text.strip()
        return final_answer