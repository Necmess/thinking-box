# Thinking Box MCP 서버 - 빠른 시작 가이드

## 🚀 5분 안에 시작하기

### 1단계: 설치 (1분)
```bash
cd thinking_box_mcp
pip install -r requirements.txt
```

### 2단계: Notion 설정 (2분)

#### Notion Integration 생성
1. https://www.notion.so/my-integrations 접속
2. "+ New integration" 클릭
3. 이름 입력 (예: "Thinking Box")
4. "Submit" 클릭
5. **Internal Integration Token** 복사 (secret_로 시작)

#### Database 생성
1. Notion에서 새 페이지 생성
2. "/database" 입력 → "Table - Inline" 선택
3. 다음 속성(columns) 추가:
   ```
   Title          (기본 제공 - title)
   Idea Stage     (Select - 옵션: 발산, 수렴)
   Summary        (Text)
   Key Points     (Multi-select)
   Tasks          (Text)
   Confidence     (Number)
   Session ID     (Text)
   Created At     (Date)
   ```
4. 우측 상단 "Share" → Integration 추가 ("Thinking Box" 선택)
5. 브라우저 URL에서 Database ID 복사
   - URL: `notion.so/{workspace}/{DATABASE_ID}?v=...`
   - 32자 영숫자 문자열

### 3단계: 환경 변수 설정 (30초)
```bash
cp .env.example .env
nano .env  # 또는 원하는 에디터
```

`.env` 파일 내용:
```
NOTION_TOKEN=secret_여기에_토큰_붙여넣기
NOTION_DATABASE_ID=여기에_데이터베이스_ID_붙여넣기
```

### 4단계: 서버 실행 (30초)
```bash
python http_server.py
```

출력:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 5단계: 테스트 (1분)
새 터미널 열고:
```bash
python test_api.py
```

성공하면:
```
✅ 저장 성공!
페이지 URL: https://notion.so/...
```

## 🎉 완료!

이제 다음 방법으로 사용할 수 있습니다:

### 방법 1: HTTP API로 직접 호출
```python
import requests

requests.post("http://localhost:8000/ingest", json={
    "session_id": "test-001",
    "idea_stage": "발산",
    "title": "새 아이디어",
    "summary": "간단한 요약",
    "key_points": ["포인트1", "포인트2"],
    "tasks": [{"owner": "개발팀", "task": "구현"}],
    "confidence": 0.85
})
```

### 방법 2: Claude Desktop에서 사용
1. MCP 설정 추가 (README.md의 "방식 1: MCP 서버" 섹션 참고)
2. Claude Desktop 재시작
3. 프롬프트로 저장 요청

### 방법 3: Thinking Box와 통합
```bash
python integration_example.py
```

## 🔍 문제 해결

### "Connection refused"
→ 서버가 실행 중인지 확인: `python http_server.py`

### "Notion API error"
→ `.env` 파일의 토큰/DB ID 확인

### "Database not found"
→ Integration이 Database에 추가되었는지 확인

## 📚 더 알아보기

- **전체 문서**: `README.md`
- **아키텍처**: `ARCHITECTURE.md`
- **API 문서**: http://localhost:8000/docs (서버 실행 후)

## 💡 다음 단계

1. **실제 데이터로 테스트**: 회의록을 입력해보세요
2. **Thinking Box 통합**: 원래의 에이전트와 연결
3. **커스터마이징**: 프롬프트나 Database 스키마 수정
4. **확장**: STT, 멀티유저, 자동화 등 추가

질문이나 이슈가 있다면 GitHub Issues로 문의하세요!
