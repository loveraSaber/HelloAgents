from LLM.HelloAgentsLLM import HelloAgentsLLM
from planner.Planner import Planner
from executor.planexecutor import planExecutor
class PlanAndSolveAgent:
    def __init__(self, llm_client: HelloAgentsLLM):
        self.llm_client = llm_client
        self.planner = Planner(self.llm_client)
        self.solver = planExecutor(self.llm_client)
    def act(self, question:str) -> str:
        print(f"🔍 问题: {question}")
        plan = self.planner.plan(question)
        if not plan:
            print("❌ 计划生成失败，无法继续执行。")
            return None
        print(f"✅ 计划生成成功，计划内容:\n{plan}")
        answer = self.solver.execute(question, plan)
        print(f"🎯 最终答案: {answer}")
        return answer