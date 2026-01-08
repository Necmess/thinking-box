# Thinking Box MCP 서버 - 프로젝트 요약

## 📦 프로젝트 개요

**Thinking Box MCP 서버**는 LLM 에이전트의 사고 결과를 Notion Database에 자동으로 저장하는 시스템입니다.

- **목표**: 에이전트 출력(JSON) → Notion 구조화 저장
- **방식**: MCP 표준 또는 HTTP REST API
- **단계**: MVP (단일 워크스페이스, 단일 Database)

## 🎯 핵심 가치

1. **표준화**: Anthropic MCP 프로토콜 준수
2. **유연성**: 2가지 사용 방식 (MCP/HTTP API)
3. **단순성**: 최소 기능에 집중
4. **확장성**: 향후 확장 가능한 구조

## 🏗️ 시스템 구성

```
Thinking Box Agent (JSON 출력)
         ↓
    MCP 서버
    ├── 방식 1: stdio MCP (Claude Desktop)
    └── 방식 2: HTTP API (외부 시스템)
         ↓
    Notion Database (구조화 저장)
```

## 📂 파일 구조

```
thinking_box_mcp/
├── 📄 핵심 모듈
│   ├── mcp_server.py          # MCP 서버 (stdio)
│   ├── http_server.py         # HTTP REST API
│   └── notion_storage.py      # Notion 연동
│
├── 🧪 테스트/예시
│   ├── test_api.py            # API 테스트
│   └── integration_example.py # 통합 예시
│
├── 📚 문서
│   ├── README.md              # 전체 가이드
│   ├── QUICKSTART.md          # 5분 시작 가이드
│   └── ARCHITECTURE.md        # 상세 아키텍처
│
└── ⚙️ 설정
    ├── requirements.txt       # 의존성
    ├── .env.example           # 환경 변수 템플릿
    └── claude_desktop_config.json  # MCP 설정
```

## 🚀 사용 방식

### ⭐ 완전 통합 버전 (추천!)
```bash
# 회의록 → Thinking Box 분석 → Notion 저장 (자동)
python run.py                    # 대화형 모드
python run.py meeting.txt        # 파일 입력
```
→ 한 번에 전체 파이프라인 실행!

자세한 사용법: **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)**

### 방식 1: MCP 서버 (Claude Desktop)
```bash
# 설정 파일에 추가
~/Library/Application Support/Claude/claude_desktop_config.json

# Claude Desktop에서 tool 호출
"Notion에 저장해줘: {JSON 데이터}"
```

### 방식 2: HTTP REST API
```bash
# 서버 실행
python http_server.py

# HTTP POST 요청
curl -X POST http://localhost:8000/ingest -d '{...}'
```

## 💾 Notion 스키마

| 속성 | 타입 | 설명 |
|------|------|------|
| Title | title | 아이디어 제목 |
| Idea Stage | select | 발산/수렴 |
| Summary | rich_text | 요약 |
| Key Points | multi_select | 핵심 포인트 |
| Tasks | rich_text | 작업 목록 |
| Confidence | number | 신뢰도 (0~1) |
| Session ID | rich_text | 세션 ID |
| Created At | date | 생성 시간 |

## 🔧 기술 스택

- **언어**: Python 3.8+
- **MCP SDK**: Anthropic MCP 1.0+
- **웹 프레임워크**: FastAPI
- **Notion SDK**: notion-client 2.2+
- **검증**: Pydantic 2.5+

## 📊 데이터 플로우

```
1. JSON 입력
   {
     "title": "아이디어",
     "summary": "요약",
     "key_points": [...],
     "tasks": [...],
     "confidence": 0.87
   }

2. MCP Tool 호출 또는 HTTP POST

3. Notion 포맷 변환
   properties = {
     "Title": {"title": [...]},
     "Idea Stage": {"select": {...}},
     ...
   }

4. Notion API 저장
   POST /v1/pages

5. 결과 반환
   {
     "page_url": "https://notion.so/...",
     "page_id": "abc123...",
     "success": true
   }
```

## ✅ 완료 사항 (MVP)

- [x] Notion 연동 모듈
- [x] MCP 서버 (stdio)
- [x] HTTP REST API
- [x] 데이터 검증 (Pydantic)
- [x] 에러 처리
- [x] 테스트 스크립트
- [x] 통합 예시
- [x] 상세 문서화

## 🔮 확장 계획

### 단기 (1-2주)
- [ ] Thinking Box 에이전트 완전 통합
- [ ] STT 입력 지원
- [ ] 배치 저장 기능

### 중기 (1개월)
- [ ] 멀티 Database 지원
- [ ] 사용자 인증/권한
- [ ] 실시간 대시보드

### 장기 (3개월+)
- [ ] 멀티 워크스페이스
- [ ] 자동 요약/리마인더
- [ ] Slack/Discord 통합
- [ ] AI 기반 분석 및 인사이트

## 🎓 학습 포인트

### MCP 프로토콜 이해
- stdio 기반 JSON-RPC 통신
- Tool/Resource/Prompt 개념
- Claude Desktop 연동 방법

### Notion API 활용
- Database 생성 및 관리
- Properties 타입별 포맷
- Integration 권한 관리

### FastAPI 패턴
- Pydantic 모델 검증
- 자동 API 문서 생성
- 비동기 처리

## 🤝 기여 포인트

1. **프롬프트 최적화**: Thinking Box 에이전트 프롬프트 개선
2. **UI 개발**: 실시간 모니터링 대시보드
3. **통합 확장**: Slack, Discord, MS Teams 등
4. **성능 개선**: 배치 처리, 캐싱, 최적화

## 📈 성과 지표

- ✅ 2가지 사용 방식 구현 (MCP + HTTP)
- ✅ 완전한 문서화 (3개 가이드)
- ✅ 테스트 스크립트 포함
- ✅ 5분 내 시작 가능
- ✅ 확장 가능한 아키텍처

## 🔗 관련 링크

- **MCP Spec**: https://spec.modelcontextprotocol.io/
- **Notion API**: https://developers.notion.com/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Thinking Box**: (원본 프로젝트 링크)

## 💬 피드백 & 문의

이슈나 개선 사항이 있다면:
1. GitHub Issues 등록
2. Pull Request 제출
3. 문서 개선 제안

---

**버전**: 1.0.0 (MVP)  
**업데이트**: 2025-01-08  
**상태**: ✅ 프로덕션 준비 (MVP)
