# Thinking Box MCP 서버 - 아키텍처 상세

## 🎯 MCP(Model Context Protocol)란?

**MCP**는 Anthropic이 개발한 표준 프로토콜로, LLM 애플리케이션이 외부 데이터 소스 및 도구와 통합할 수 있게 합니다.

### MCP의 핵심 특징
- **표준화**: 일관된 인터페이스로 다양한 도구 통합
- **Stdio 기반**: JSON-RPC 프로토콜 사용
- **3가지 기본 요소**:
  1. **Tools**: 실행 가능한 함수
  2. **Resources**: 읽기 가능한 데이터
  3. **Prompts**: 재사용 가능한 프롬프트 템플릿

### 왜 MCP를 사용하는가?

**기존 방식 (HTTP API)**:
```
LLM → HTTP POST → 서버 → Notion
```
- LLM이 직접 API 호출 로직 작성 필요
- 에러 처리, 재시도 로직 복잡
- 각 통합마다 별도 구현

**MCP 방식**:
```
LLM → MCP Tool 호출 → MCP 서버 → Notion
```
- LLM은 "save_thinking_result" tool만 호출
- 서버가 복잡한 로직 처리
- 표준화된 인터페이스

## 🏗️ 전체 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                     사용자                              │
│  - 회의 진행                                            │
│  - 아이디어 브레인스토밍                                │
└────────────────┬────────────────────────────────────────┘
                 │
                 ↓ (음성 또는 텍스트)
┌────────────────────────────────────────────────────────┐
│            Thinking Box Agent                          │
│  ┌──────────────────────────────────────────────┐     │
│  │  Agent 1: 입력 정제                         │     │
│  │  - 노이즈 제거                              │     │
│  │  - 세그먼트 분리                            │     │
│  └──────────────┬───────────────────────────────┘     │
│                 ↓                                      │
│  ┌──────────────────────────────────────────────┐     │
│  │  Agent 2: 아이디어 추출                     │     │
│  │  - 분류 (제안/가설/질문/관찰)              │     │
│  │  - 중요도 순위화                            │     │
│  └──────────────┬───────────────────────────────┘     │
│                 ↓                                      │
│  ┌──────────────────────────────────────────────┐     │
│  │  Agent 3: 계획 구조화                       │     │
│  │  - 문제 정의                                │     │
│  │  - 솔루션 방향                              │     │
│  │  - 실행 단계                                │     │
│  └──────────────┬───────────────────────────────┘     │
│                 │                                      │
│                 ↓ JSON 출력                            │
│  {                                                     │
│    "session_id": "...",                                │
│    "idea_stage": "발산",                              │
│    "title": "...",                                     │
│    "summary": "...",                                   │
│    "key_points": [...],                                │
│    "tasks": [...],                                     │
│    "confidence": 0.87                                  │
│  }                                                     │
└────────────────┬───────────────────────────────────────┘
                 │
                 ↓
┌────────────────────────────────────────────────────────┐
│              MCP 서버 레이어                           │
│                                                        │
│  ┌──────────────────────┐  ┌─────────────────────┐   │
│  │   방식 1: MCP 서버   │  │  방식 2: HTTP API  │   │
│  │   (stdio 기반)       │  │  (REST API)        │   │
│  ├──────────────────────┤  ├─────────────────────┤   │
│  │ - JSON-RPC           │  │ - POST /ingest     │   │
│  │ - Claude Desktop 연동│  │ - FastAPI          │   │
│  │ - Tool:              │  │ - Swagger UI       │   │
│  │   save_thinking_     │  │ - 외부 시스템 통합 │   │
│  │   result             │  │                     │   │
│  └──────────┬───────────┘  └──────────┬──────────┘   │
│             │                         │               │
│             └──────────┬──────────────┘               │
│                        ↓                               │
│            ┌────────────────────────┐                 │
│            │  Notion Storage 모듈   │                 │
│            │  - API 호출            │                 │
│            │  - 데이터 변환         │                 │
│            │  - 에러 처리           │                 │
│            └────────────┬───────────┘                 │
└─────────────────────────┼──────────────────────────────┘
                          │
                          ↓ HTTPS
┌─────────────────────────────────────────────────────────┐
│                    Notion API                           │
│  POST /v1/pages                                         │
│  {                                                      │
│    "parent": {"database_id": "..."},                    │
│    "properties": {                                      │
│      "Title": {...},                                    │
│      "Idea Stage": {...},                               │
│      "Summary": {...},                                  │
│      ...                                                │
│    }                                                    │
│  }                                                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                 Notion Database                         │
│  ┌───────────────────────────────────────────────┐     │
│  │ Title | Stage | Summary | Points | Tasks | ... │     │
│  ├───────────────────────────────────────────────┤     │
│  │  ...  │  ...  │   ...   │  ...   │  ...  │... │     │
│  └───────────────────────────────────────────────┘     │
│  - 검색/필터 가능                                       │
│  - 뷰 커스터마이징                                      │
│  - 팀 협업                                              │
└─────────────────────────────────────────────────────────┘
```

## 🔄 데이터 변환 플로우

### 1단계: 에이전트 출력 (JSON)
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "idea_stage": "발산",
  "title": "AI 협업 에디터",
  "summary": "실시간 협업 + AI 제안 기능을 결합한 에디터",
  "key_points": ["실시간 편집", "AI 자동완성", "충돌 해결"],
  "tasks": [
    {"owner": "FE", "task": "UI 구현"},
    {"owner": "BE", "task": "WebSocket 서버"}
  ],
  "confidence": 0.87
}
```

### 2단계: MCP 서버 수신
```python
# MCP Tool 호출
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "save_thinking_result":
        result = notion_client.save_thinking_result(arguments)
        return [TextContent(text=f"저장 완료: {result['page_url']}")]
```

### 3단계: Notion 포맷 변환
```python
# notion_storage.py에서 변환
properties = {
    "Title": {
        "title": [{"text": {"content": "AI 협업 에디터"}}]
    },
    "Idea Stage": {
        "select": {"name": "발산"}
    },
    "Summary": {
        "rich_text": [{"text": {"content": "실시간 협업 + ..."}}]
    },
    "Key Points": {
        "multi_select": [
            {"name": "실시간 편집"},
            {"name": "AI 자동완성"},
            {"name": "충돌 해결"}
        ]
    },
    "Tasks": {
        "rich_text": [{"text": {"content": "[FE] UI 구현\n[BE] WebSocket 서버"}}]
    },
    "Confidence": {
        "number": 0.87
    },
    "Created At": {
        "date": {"start": "2025-01-08T12:00:00.000Z"}
    }
}
```

### 4단계: Notion API 호출
```python
response = notion_client.pages.create(
    parent={"database_id": database_id},
    properties=properties
)
# 반환: page_id, page_url, created_time
```

## 🔧 모듈 설계

### 1. `notion_storage.py` - Notion 연동 모듈

**책임**:
- Notion API 래핑
- 데이터 포맷 변환
- 에러 처리

**핵심 메서드**:
```python
class NotionStorage:
    def __init__(self, token, database_id)
    def save_thinking_result(self, data: dict) -> dict
    def _build_properties(self, data: dict) -> dict
    def test_connection(self) -> bool
```

### 2. `mcp_server.py` - MCP 서버

**책임**:
- stdio 기반 JSON-RPC 통신
- Tool 정의 및 실행
- Claude Desktop 연동

**핵심 기능**:
```python
@app.list_tools()  # 사용 가능한 도구 목록
async def list_tools() -> list[Tool]

@app.call_tool()   # 도구 실행
async def call_tool(name: str, arguments: Any) -> list[TextContent]
```

### 3. `http_server.py` - HTTP REST API

**책임**:
- HTTP 엔드포인트 제공
- 요청 검증 (Pydantic)
- API 문서 자동 생성 (Swagger)

**핵심 엔드포인트**:
```python
GET  /              # 서비스 정보
GET  /health        # 상태 확인
POST /ingest        # 데이터 저장
```

## 🔐 보안 고려사항 (향후)

### 현재 (MVP)
- ✅ 환경 변수로 토큰 관리
- ❌ 인증 없음
- ❌ Rate limiting 없음
- ❌ 입력 검증 최소화

### 프로덕션 고려사항
1. **인증/권한**
   - API Key 기반 인증
   - 사용자별 Notion 토큰 관리
   
2. **Rate Limiting**
   - 요청 빈도 제한
   - Notion API quota 관리

3. **입력 검증**
   - XSS 방지
   - SQL Injection 방지
   - 데이터 크기 제한

4. **로깅/모니터링**
   - 요청 로그
   - 에러 추적
   - 성능 모니터링

## 📈 확장 시나리오

### 시나리오 1: 멀티 워크스페이스
```python
# 조직별 Database 관리
workspaces = {
    "company_a": {
        "notion_token": "...",
        "databases": {
            "project_x": "db_id_1",
            "project_y": "db_id_2"
        }
    }
}
```

### 시나리오 2: STT 통합
```
음성 입력 → STT → 텍스트 → Thinking Box → MCP → Notion
```

### 시나리오 3: 실시간 대시보드
```
MCP 서버 → WebSocket → 프론트엔드 대시보드
- 실시간 저장 상태 표시
- 저장된 아이디어 시각화
```

### 시나리오 4: 자동 요약 및 리마인더
```
Notion → Slack 통합 → 주간 요약 자동 전송
```

## 🎯 MVP vs 프로덕션 비교

| 기능 | MVP (현재) | 프로덕션 |
|------|-----------|---------|
| 인증 | ❌ 없음 | ✅ API Key / OAuth |
| Database | 단일 | 멀티 (프로젝트별) |
| 사용자 | 단일 | 멀티테넌트 |
| 에러 처리 | 기본 | 상세 + 재시도 |
| 로깅 | 최소 | 상세 + 모니터링 |
| 배포 | 로컬 | Docker + K8s |
| 스케일링 | N/A | 수평 확장 |

## 💡 설계 원칙

1. **단순성**: MVP는 최소 기능에 집중
2. **모듈성**: 각 모듈은 독립적으로 교체 가능
3. **확장성**: 향후 기능 추가가 용이한 구조
4. **표준 준수**: MCP 프로토콜 표준 준수

## 🔍 디버깅 가이드

### MCP 서버 디버깅
```bash
# MCP 서버 직접 실행 (stdio 모드)
python mcp_server.py

# 입력 예시 (JSON-RPC)
{"jsonrpc": "2.0", "method": "tools/list", "id": 1}
```

### HTTP API 디버깅
```bash
# 서버 로그 확인
python http_server.py

# curl로 테스트
curl -X POST http://localhost:8000/ingest -H "Content-Type: application/json" -d @test_data.json
```

### Notion API 디버깅
```python
# 직접 테스트
from notion_storage import NotionStorage

storage = NotionStorage()
print(storage.test_connection())  # True/False
```

## 📚 참고 자료

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Notion API Documentation](https://developers.notion.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
