import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Agent.PlanAndSolveAgent import PlanAndSolveAgent
from tools.search import search

# tool_executor = ToolExecutor()
# search_description="使用SerpApi进行网页搜索，输入搜索关键词，返回相关的搜索结果摘要。" 
# tool_executor.register_tool("Search",search,tool_desc=search_description)
# print("\n--- 已注册工具 ---")
# print(tool_executor.getAviableTools())
# print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
# tool_name = "Search"
# tool_input = "英伟达最新的GPU型号是什么"

# tool_function = tool_executor.gettool(tool_name)
# if tool_function:
#     observation = tool_function(tool_input)
#     print("--- 观察 (Observation) ---")
#     print(observation)
# else:
#     print(f"错误:未找到名为 '{tool_name}' 的工具。")
# from LLM.HelloAgentsLLM import HelloAgentsLLM
# llm_client = HelloAgentsLLM()
# agent = PlanAndSolveAgent(llm_client)
# question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
# response=agent.act(question)
from Agent.ReflectionAgent import ReflectionAgent
from LLM.HelloAgentsLLM import HelloAgentsLLM
agent = ReflectionAgent(HelloAgentsLLM())
question = "编写一个Python函数，找出1到n之间所有的素数 (prime numbers)。"
response=agent.run(question)
