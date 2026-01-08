"""
LLM 호출을 위한 간단한 래퍼
"""
import os
from anthropic import Anthropic


class LLMClient:
    def __init__(self, model="claude-sonnet-4-20250514"):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model
    
    def call(self, system_prompt: str, user_message: str, max_tokens: int = 4000) -> str:
        """
        LLM 호출 후 텍스트 응답 반환
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return response.content[0].text
