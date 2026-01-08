"""
Thinking Box MCP 서버 테스트 스크립트

HTTP API 엔드포인트를 테스트
"""
import requests
import json
from datetime import datetime


# 테스트 데이터
test_data = {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "idea_stage": "발산",
    "title": "AI 기반 실시간 협업 에디터",
    "summary": "여러 사용자가 동시에 문서를 편집하면서 AI가 실시간으로 제안을 제공하는 협업 도구",
    "key_points": [
        "실시간 동시 편집 지원",
        "AI 자동 완성 및 제안",
        "버전 관리 자동화",
        "충돌 해결 지능화"
    ],
    "tasks": [
        {"owner": "FE", "task": "실시간 동기화 UI 구현"},
        {"owner": "BE", "task": "WebSocket 서버 구축"},
        {"owner": "AI", "task": "LLM 통합 및 프롬프트 설계"},
        {"owner": "DevOps", "task": "인프라 스케일링 계획"}
    ],
    "confidence": 0.87
}


def test_health():
    """헬스 체크 테스트"""
    print("=" * 60)
    print("🏥 헬스 체크 테스트")
    print("=" * 60)
    
    response = requests.get("http://localhost:8000/health")
    print(f"상태 코드: {response.status_code}")
    print(f"응답:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def test_ingest():
    """데이터 저장 테스트"""
    print("=" * 60)
    print("📤 데이터 저장 테스트")
    print("=" * 60)
    
    print("전송 데이터:")
    print(json.dumps(test_data, indent=2, ensure_ascii=False))
    print()
    
    response = requests.post(
        "http://localhost:8000/ingest",
        json=test_data
    )
    
    print(f"상태 코드: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print("✅ 저장 성공!")
        print(f"페이지 URL: {result['page_url']}")
        print(f"페이지 ID: {result['page_id']}")
        print(f"생성 시간: {result['created_time']}")
    else:
        print("❌ 저장 실패!")
        print(f"에러: {response.json()}")
    print()


def test_invalid_data():
    """잘못된 데이터 테스트"""
    print("=" * 60)
    print("🚫 잘못된 데이터 테스트")
    print("=" * 60)
    
    invalid_data = {
        "session_id": "test",
        "idea_stage": "잘못된_단계",  # 발산/수렴이 아님
        "title": "테스트",
        "summary": "요약",
        "confidence": 1.5  # 0~1 범위 초과
    }
    
    response = requests.post(
        "http://localhost:8000/ingest",
        json=invalid_data
    )
    
    print(f"상태 코드: {response.status_code}")
    print(f"예상대로 에러 발생: {response.status_code == 422}")
    print(f"에러 상세:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def main():
    """전체 테스트 실행"""
    print("\n🧪 Thinking Box MCP 서버 테스트 시작\n")
    
    try:
        # 1. 헬스 체크
        test_health()
        
        # 2. 정상 데이터 저장
        test_ingest()
        
        # 3. 잘못된 데이터
        test_invalid_data()
        
        print("=" * 60)
        print("✅ 모든 테스트 완료!")
        print("=" * 60)
    
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다.")
        print("먼저 서버를 실행하세요: python http_server.py")
    
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")


if __name__ == "__main__":
    main()
