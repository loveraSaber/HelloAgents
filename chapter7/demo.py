from hello_agents import SimpleAgent,HelloAgentsLLM
from my_llm import MyLLM
from dotenv import load_dotenv
load_dotenv()
import os
# llm=HelloAgentsLLM(
#     base_url=os.getenv("MODEL_URL"),
#     api_key=os.getenv("API_KEY"),
#     model=os.getenv("MODEL_NAME")
# )
llm_client=MyLLM(provider="siliconflow")
agent=SimpleAgent(
    name="AI助手",
    llm=llm_client,
    system_prompt="你是一个乐于助人的AI助手，帮助用户解答问题和提供建议。"
)
response=agent.run("请介绍一下自己？")
print(response)