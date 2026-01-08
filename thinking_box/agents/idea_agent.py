"""
Agent 2: 아이디어 추출 및 재순위화 에이전트
"""
from core.llm_client import LLMClient
from prompts.templates import IDEA_EXTRACTION_SYSTEM, IDEA_EXTRACTION_USER


class IdeaAgent:
    """
    정제된 대화에서 핵심 아이디어를 추출하고 중요도 순으로 재순위화
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
    
    def process(self, cleaned_conversation: str) -> str:
        """
        정제된 대화에서 아이디어 후보를 추출하고 순위화
        
        Args:
            cleaned_conversation: Agent 1의 출력 (정제된 대화)
            
        Returns:
            순위화된 아이디어 리스트
        """
        print("💡 Agent 2: 아이디어 추출 및 순위화 중...")
        
        user_message = IDEA_EXTRACTION_USER.format(
            cleaned_conversation=cleaned_conversation
        )
        ranked_ideas = self.llm.call(
            system_prompt=IDEA_EXTRACTION_SYSTEM,
            user_message=user_message,
            max_tokens=3000
        )
        
        print("✓ 아이디어 추출 완료\n")
        return ranked_ideas
