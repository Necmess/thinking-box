"""
Agent 1: 입력 이해 및 정제 에이전트
"""
from core.llm_client import LLMClient
from prompts.templates import INPUT_CLEANING_SYSTEM, INPUT_CLEANING_USER


class InputAgent:
    """
    원본 대화/회의 내용에서 노이즈를 제거하고 구조화
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def process(self, raw_input: str) -> str:
        """
        원본 입력을 정제하여 구조화된 대화 텍스트로 변환
        
        Args:
            raw_input: STT 출력 또는 원본 대화 텍스트
            
        Returns:
            정제되고 세그먼트화된 대화 텍스트
        """
        print("🔍 Agent 1: 입력 정제 중...")
        
        user_message = INPUT_CLEANING_USER.format(raw_input=raw_input)
        cleaned = self.llm.call(
            system_prompt=INPUT_CLEANING_SYSTEM,
            user_message=user_message,
            max_tokens=3000
        )
        
        print("✓ 정제 완료\n")
        return cleaned
