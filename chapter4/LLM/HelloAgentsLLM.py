import os
import openai
from dotenv import load_dotenv
from typing import List, Dict

# 加载 .env 文件中的环境变量
load_dotenv()

class HelloAgentsLLM:
    """
    为本书 "Hello Agents" 定制的LLM客户端。
    它用于调用任何兼容OpenAI接口的服务，并默认使用流式响应。
    """
    def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None):
        """
        初始化客户端。优先使用传入参数，如果未提供，则从环境变量加载。
        """
        self.model = model or os.getenv("MODEL_NAME")
        apiKey = apiKey or os.getenv("API_KEY")
        baseUrl = baseUrl or os.getenv("MODEL_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))
        
        if not all([self.model, apiKey, baseUrl]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")

        if hasattr(openai, "OpenAI"):
            self.client = openai.OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)
            self.use_new_client = True
        else:
            openai.api_key = apiKey
            openai.api_base = baseUrl
            openai.timeout = timeout
            self.client = openai
            self.use_new_client = False

    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        调用大语言模型进行思考，并返回其响应。
        """
        print(f"🧠 正在调用 {self.model} 模型...")
        try:
            if self.use_new_client:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    stream=True,
                )
            else:
                response = self.client.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    stream=True,
                )

            # 处理流式响应
            print("✅ 大语言模型响应成功:")
            collected_content = []
            for chunk in response:
                if not getattr(chunk, 'choices', None):
                    continue
                # 新旧 SDK 都支持 chunk.choices[0].delta.content 或 chunk.choices[0].text
                delta = chunk.choices[0]
                content = getattr(delta, 'delta', None)
                if content is not None:
                    content = content.content or ""
                else:
                    content = getattr(delta, 'text', "") or ""
                print(content, end="", flush=True)
                collected_content.append(content)
            print()  # 在流式输出结束后换行
            return "".join(collected_content)

        except Exception as e:
            print(f"❌ 调用LLM API时发生错误: {e}")
            return None