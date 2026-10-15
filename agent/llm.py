import time
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    def __init__(self, model="qwen-plus"):
        self.model = model
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            print("  [警告] 没有找到API密钥")
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.max_retries = 3
        self.retry_delay = 2

    def chat(self, messages, temperature=0.7):
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=4096,
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"  LLM调用失败 (第{attempt}次): {e}")
                if attempt < self.max_retries:
                    print(f"  {self.retry_delay}秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    return f"[错误] LLM调用失败，已重试{self.max_retries}次: {e}"