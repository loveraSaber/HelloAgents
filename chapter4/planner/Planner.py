import os
import ast
from LLM.HelloAgentsLLM import HelloAgentsLLM

class Planner:
    def __init__(self, llm_client: HelloAgentsLLM):
        self.llm_client = llm_client

    def read_prompt(self, file_name: str) -> str:
        template_dir = os.path.join(os.path.dirname(__file__), "..", "template")
        file_path = os.path.join(template_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def plan(self, question: str) -> list[str]:
        prompt = self.read_prompt("planner.txt").format(question=question)
        messages=[{"role":"system","content":prompt}]
        print("🧠 生成计划中...")
        response_text=self.llm_client.think(messages=messages) or ""
        print(f"📋 生成的计划:\n{response_text}")

        plan_text = response_text.strip()
        if not plan_text:
            print("❌ 解析计划时出错: 响应为空")
            return []

        # 支持多种输出格式：```python[...]```, ```[...]```, 或者直接的列表文本
        for start_token, end_token in [("```python", "```"), ("```", "```")]:
            if start_token in plan_text:
                try:
                    plan_text = plan_text.split(start_token, 1)[1].split(end_token, 1)[0].strip()
                    break
                except Exception:
                    continue

        if plan_text.startswith("[") and plan_text.endswith("]"):
            try:
                plan = ast.literal_eval(plan_text)
                if isinstance(plan, list):
                    return plan
                print(f"❌ 解析计划时出错: 解析结果不是列表，类型为 {type(plan)}")
                return []
            except Exception as e:
                print(f"❌ 解析计划时出错: {e}")
                return []

        start = plan_text.find("[")
        end = plan_text.rfind("]")
        if start != -1 and end != -1 and end > start:
            try:
                plan = ast.literal_eval(plan_text[start:end+1])
                if isinstance(plan, list):
                    return plan
            except Exception as e:
                print(f"❌ 解析计划时出错: {e}")

        print("❌ 解析计划时出错: 未能识别列表格式的计划")
        return []