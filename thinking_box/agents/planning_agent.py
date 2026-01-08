"""
Agent 3: 계획 및 구조화 에이전트
"""
from core.llm_client import LLMClient
from prompts.templates import PLANNING_SYSTEM, PLANNING_USER


class PlanningAgent:
    """
    추출된 아이디어를 구조화된 사고 문서로 변환
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def process(self, ranked_ideas: str) -> str:
        """
        순위화된 아이디어를 실행 가능한 계획 문서로 구조화
        
        Args:
            ranked_ideas: Agent 2의 출력 (순위화된 아이디어)
            
        Returns:
            구조화된 계획 문서 (마크다운)
        """
        print("📋 Agent 3: 계획 구조화 중...")
        
        user_message = PLANNING_USER.format(ranked_ideas=ranked_ideas)
        planning_doc = self.llm.call(
            system_prompt=PLANNING_SYSTEM,
            user_message=user_message,
            max_tokens=4000
        )
        
        print("✓ 계획 문서 생성 완료\n")
        return planning_doc
