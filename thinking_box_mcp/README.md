# Thinking Box MCP 서버

Thinking Box 에이전트의 출력 결과를 Notion Database에 저장하는 MCP 서버

## 완전 통합 버전

**이제 Thinking Box와 완전히 통합되었습니다!**

```
회의록 입력 → Thinking Box 분석 → 자동 Notion 저장
```

**원클릭 실행**: `python run.py`

자세한 내용은 **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** 참고

## 목표

LLM 에이전트가 생성한 사고 결과(JSON)를 구조화하여 Notion에 자동 저장

## 아키텍처

```
┌─────────────────────┐
│  Thinking Box       │
│  Agent              │
│  (LLM 기반 사고)    │
└──────────┬──────────┘
           │ JSON 출력
           ↓
┌──────────────────────────────────────────┐
│         MCP 서버 (2가지 방식)             │
├──────────────────────────────────────────┤
│                                          │
│  방식 1: 실제 MCP 서버 (stdio)          │
│  - Claude Desktop 직접 연동             │
│  - save_thinking_result tool 제공       │
│                                          │
│  방식 2: HTTP REST API                  │
│  - POST /ingest 엔드포인트              │
│  - 외부 시스템 통합용                   │
│                                          │
└──────────┬───────────────────────────────┘
           │ Notion API 호출
           ↓
┌──────────────────────┐
│  Notion Database     │
│  - 구조화된 저장     │
│  - 검색/필터 가능    │
└──────────────────────┘
```

## 설치

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일 편집하여 Notion 토큰/DB ID 입력
```

## Notion 설정

### 1. Integration 생성

1. https://www.notion.so/my-integrations 접속
2. "New integration" 생성
3. `NOTION_TOKEN` 복사 (secret\_로 시작)

### 2. Database 생성 및 연결

1. Notion에서 새 Database 생성
2. 다음 속성(Properties) 추가:
   - **Title** (title)
   - **Idea Stage** (select) - 옵션: 발산, 수렴
   - **Summary** (rich_text)
   - **Key Points** (multi_select)
   - **Tasks** (rich_text)
   - **Confidence** (number)
   - **Session ID** (rich_text)
   - **Created At** (date)
3. Database 공유 → Integration 추가
4. Database ID 복사 (URL에서 확인)
   - URL 형식: `notion.so/{workspace}/{DATABASE_ID}?v=...`

## 사용법

### 방식 1: MCP 서버 (Claude Desktop)

#### 1단계: MCP 서버 설정

`claude_desktop_config.json` 파일을 Claude Desktop 설정에 추가:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "thinking-box": {
      "command": "python",
      "args": ["/절대경로/thinking_box_mcp/mcp_server.py"],
      "env": {
        "NOTION_TOKEN": "your_token_here",
        "NOTION_DATABASE_ID": "your_db_id_here"
      }
    }
  }
}
```

#### 2단계: Claude Desktop에서 사용

1. Claude Desktop 재시작
2. MCP 연결 확인 (🔌 아이콘)
3. 프롬프트 예시:

```
다음 내용을 Notion에 저장해줘:

{
  "session_id": "test-001",
  "idea_stage": "발산",
  "title": "신규 기능 아이디어",
  "summary": "사용자 경험 개선을 위한 제안",
  "key_points": ["UX 개선", "성능 최적화"],
  "tasks": [
    {"owner": "FE", "task": "UI 설계"},
    {"owner": "BE", "task": "API 개발"}
  ],
  "confidence": 0.85
}
```

### 방식 2: HTTP REST API

#### 1단계: 서버 실행

```bash
python http_server.py
# 또는
uvicorn http_server:app --reload --port 8000
```

#### 2단계: HTTP 요청

```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "idea_stage": "발산",
    "title": "AI 협업 에디터",
    "summary": "실시간 협업 + AI 제안",
    "key_points": ["실시간 편집", "AI 제안"],
    "tasks": [
      {"owner": "FE", "task": "UI 구현"},
      {"owner": "BE", "task": "서버 구축"}
    ],
    "confidence": 0.87
  }'
```

#### 3단계: 테스트 스크립트 실행

```bash
python test_api.py
```

## API 문서

### 엔드포인트

#### `GET /`

헬스 체크 및 서비스 정보

#### `GET /health`

서버 상태 및 Notion 연결 확인

#### `POST /ingest`

Thinking Box 결과 저장

**요청 본문**:

```json
{
  "session_id": "string",
  "idea_stage": "발산 | 수렴",
  "title": "string",
  "summary": "string",
  "key_points": ["string"],
  "tasks": [
    {"owner": "string", "task": "string"}
  ],
  "confidence": 0.0-1.0
}
```

**응답 (201)**:

```json
{
  "success": true,
  "page_id": "abc123...",
  "page_url": "https://notion.so/...",
  "created_time": "2025-01-08T12:00:00.000Z",
  "message": "데이터가 성공적으로 저장되었습니다"
}
```

### Swagger UI

서버 실행 후 http://localhost:8000/docs 접속

## 테스트

```bash
# 1. 서버 실행
python http_server.py

# 2. 다른 터미널에서 테스트
python test_api.py
```

## 프로젝트 구조

```
thinking_box_mcp/
├── mcp_server.py              # MCP 서버 (stdio 기반)
├── http_server.py             # HTTP REST API (FastAPI)
├── notion_storage.py          # Notion 연동 모듈
├── test_api.py                # 테스트 스크립트
├── requirements.txt           # 의존성
├── .env.example               # 환경 변수 템플릿
├── claude_desktop_config.json # MCP 설정 예시
└── README.md
```

## 🔧 확장 포인트

### 1. STT 통합

```python
# 음성 → 텍스트 → Thinking Box → MCP → Notion
from speech_recognition import Recognizer

def process_audio_to_notion(audio_file):
    text = transcribe(audio_file)
    thinking_result = thinking_box_agent.process(text)
    save_to_notion(thinking_result)
```

### 2. 사용자 분리

```python
# Database ID를 사용자별로 분리
user_databases = {
    "user1": "database_id_1",
    "user2": "database_id_2"
}

@app.post("/ingest/{user_id}")
async def ingest(user_id: str, data: ThinkingResult):
    db_id = user_databases[user_id]
    notion = NotionStorage(database_id=db_id)
    return notion.save_thinking_result(data.dict())
```

### 3. 멀티 Database 지원

```python
# 프로젝트별 Database 자동 생성
def get_or_create_database(project_name):
    # 프로젝트명으로 DB 검색 또는 생성
    pass
```

### 4. 실시간 스트리밍

```python
# WebSocket으로 실시간 저장 상태 전송
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # 실시간 저장 진행 상황 전송
```

### 5. 배치 처리

```python
# 여러 결과를 한 번에 저장
@app.post("/ingest/batch")
async def batch_ingest(items: List[ThinkingResult]):
    results = []
    for item in items:
        result = notion_client.save_thinking_result(item.dict())
        results.append(result)
    return results
```

## 주의사항 (MVP)

현재는 예선 MVP이므로:

- ❌ 인증/권한 관리 없음
- ❌ 복잡한 에러 복구 없음
- ❌ 프로덕션 배포 고려 없음
- ✅ 단일 워크스페이스/DB 전제
- ✅ 로컬 개발 환경 중심

## 라이센스

MIT
