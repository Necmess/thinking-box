"""
Thinking Box Agent와 MCP 서버 통합 예시

원래의 Thinking Box 에이전트와 MCP 서버를 연결하는 방법
"""
import json
import requests
from typing import Dict, Any


class ThinkingBoxIntegration:
    """
    Thinking Box 에이전트와 MCP 서버를 연결하는 통합 클래스
    """
    
    def __init__(self, mcp_api_url: str = "http://localhost:8000"):
        """
        Args:
            mcp_api_url: MCP HTTP API 서버 주소
        """
        self.api_url = mcp_api_url
    
    def process_and_save(self, raw_conversation: str) -> Dict[str, Any]:
        """
        대화 입력 → Thinking Box 처리 → Notion 저장
        
        Args:
            raw_conversation: 원본 회의/대화 텍스트
            
        Returns:
            저장 결과 (Notion page URL 등)
        """
        # 1단계: Thinking Box Agent로 처리
        print("🧠 Thinking Box 에이전트 처리 중...")
        thinking_result = self._run_thinking_box(raw_conversation)
        
        # 2단계: MCP 서버로 Notion에 저장
        print("💾 Notion에 저장 중...")
        save_result = self._save_to_notion(thinking_result)
        
        return save_result
    
    def _run_thinking_box(self, raw_input: str) -> Dict[str, Any]:
        """
        Thinking Box 에이전트 실행 (시뮬레이션)
        
        실제로는 원래의 Thinking Box 파이프라인을 실행:
        - Agent 1: 입력 정제
        - Agent 2: 아이디어 추출
        - Agent 3: 계획 구조화
        
        여기서는 간단한 예시로 대체
        """
        # TODO: 실제 Thinking Box 에이전트 호출
        # from thinking_box.main import ThinkingBox
        # box = ThinkingBox()
        # results = box.run(raw_input)
        
        # 현재는 예시 데이터 반환
        return {
            "session_id": "demo-session-001",
            "idea_stage": "수렴",
            "title": "AI 기반 회의록 자동화",
            "summary": "회의 내용을 자동으로 분석하여 핵심 아이디어를 추출하고 실행 계획을 생성",
            "key_points": [
                "STT 통합 필요",
                "실시간 처리 구현",
                "Notion 자동 저장"
            ],
            "tasks": [
                {"owner": "Backend", "task": "MCP 서버 구축"},
                {"owner": "Frontend", "task": "대시보드 개발"},
                {"owner": "AI", "task": "프롬프트 최적화"}
            ],
            "confidence": 0.92
        }
    
    def _save_to_notion(self, thinking_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        MCP 서버 API를 통해 Notion에 저장
        
        Args:
            thinking_result: Thinking Box 에이전트 출력
            
        Returns:
            저장 결과
        """
        try:
            response = requests.post(
                f"{self.api_url}/ingest",
                json=thinking_result,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ 저장 완료: {result['page_url']}")
            return result
        
        except requests.exceptions.RequestException as e:
            print(f"❌ 저장 실패: {e}")
            raise


def demo_integration():
    """
    통합 데모 실행
    """
    print("=" * 60)
    print("🔗 Thinking Box + MCP 서버 통합 데모")
    print("=" * 60)
    print()
    
    # 예시 회의록
    conversation = """
    [프로젝트 킥오프 미팅]
    
    팀장: 오늘은 신규 AI 기능에 대해 논의하겠습니다.
    개발자A: 사용자가 회의 중에 실시간으로 아이디어를 기록할 수 있으면 좋겠어요.
    개발자B: 그리고 자동으로 Notion에 정리되면 업무 효율이 크게 올라갈 것 같아요.
    팀장: 좋은 아이디어네요. STT 기능도 통합해봅시다.
    """
    
    print("📝 입력 대화:")
    print(conversation)
    print()
    
    # 통합 실행
    integration = ThinkingBoxIntegration()
    
    try:
        result = integration.process_and_save(conversation)
        
        print()
        print("=" * 60)
        print("✅ 처리 완료!")
        print("=" * 60)
        print(f"Notion 페이지: {result['page_url']}")
        print(f"페이지 ID: {result['page_id']}")
        print(f"생성 시간: {result['created_time']}")
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ 처리 실패")
        print("=" * 60)
        print(f"에러: {e}")
        print()
        print("💡 해결 방법:")
        print("1. MCP 서버가 실행 중인지 확인: python http_server.py")
        print("2. Notion 토큰/DB ID가 올바른지 확인")
        print("3. 네트워크 연결 확인")


if __name__ == "__main__":
    demo_integration()
