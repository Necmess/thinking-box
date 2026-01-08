# Thinking Box 프로젝트 전체

회의록/대화를 3단계 분석하고 Notion에 자동 저장하는 통합 시스템

## 📂프로젝트 구조

```
프로젝트/
│
├── thinking_box/           # 핵심 분석 엔진
│   ├── agents/             # 3개 에이전트 (정제/아이디어/계획)
│   ├── core/               # LLM 클라이언트
│   ├── prompts/            # 프롬프트 템플릿
│   ├── main.py             # 기본 실행 (마크다운 출력)
│   └── README.md           # 상세 사용법
│
└── thinking_box_mcp/       # MCP 서버 & Notion 통합
    ├── integrated_system.py    # 완전 통합 시스템
    ├── run.py                  # ⭐ 원클릭 실행
    ├── notion_storage.py       # Notion 연동
    ├── mcp_server.py           # MCP 서버
    ├── http_server.py          # HTTP API
    ├── INTEGRATION_GUIDE.md    # 통합 가이드
    └── README.md               # MCP 서버 문서
```

## 빠른 시작 (3분)

### 1. 설치

```bash
# thinking_box 의존성
cd thinking_box
pip install -r requirements.txt

# thinking_box_mcp 의존성
cd ../thinking_box_mcp
pip install -r requirements.txt
```

### 2. 환경 변수 설정

**thinking_box/.env**:

```
ANTHROPIC_API_KEY=your_api_key_here
```

**thinking_box_mcp/.env**:

```
ANTHROPIC_API_KEY=your_api_key_here
NOTION_TOKEN=secret_your_token_here
NOTION_DATABASE_ID=your_database_id_here
```

### 3. 실행!

#### 방법 A: 마크다운 출력만

```bash
cd thinking_box
python main.py --input example_input.txt
```

#### 방법 B: Notion 자동 저장 (권장!)

```bash
cd thinking_box_mcp
python run.py
```

## 💡 사용 시나리오

### 시나리오 1: 회의록 빠른 분석

```bash
cd thinking_box
python main.py --input meeting.txt --output analysis.md
```

- 3-Agent 분석
- 마크다운 문서 생성
- 로컬 저장

### 시나리오 2: Notion 팀 공유

```bash
cd thinking_box_mcp
python run.py meeting.txt
```

- 3-Agent 분석
- JSON 자동 변환
- Notion Database 저장
- 팀 전체 공유

### 시나리오 3: HTTP API 서버

```bash
cd thinking_box_mcp
python http_server.py
```

- 외부 시스템 통합
- REST API 제공
- Swagger 문서 자동 생성

### 시나리오 4: Claude Desktop 연동

```bash
# thinking_box_mcp/claude_desktop_config.json 설정
```

- MCP 프로토콜 사용
- Claude Desktop에서 직접 호출
- save_thinking_result tool 제공

## 핵심 기능

### Thinking Box (핵심 엔진)

**3-Agent 분석**

- Agent 1: 노이즈 제거 & 구조화
- Agent 2: 아이디어 추출 & 순위화
- Agent 3: 실행 계획 구조화

**마크다운 출력**

- 정제된 대화
- 순위화된 아이디어
- 구조화된 계획

### MCP 서버 (통합 & 저장)

**완전 통합**

- Thinking Box 자동 실행
- JSON 자동 변환
- Notion 자동 저장

**3가지 사용 방식**

- 원클릭 실행 (run.py)
- MCP 서버 (Claude Desktop)
- HTTP REST API

## 데이터 플로우

```
회의록 입력
    ↓
[Thinking Box]
    ├─ Agent 1: 정제
    ├─ Agent 2: 아이디어 추출
    └─ Agent 3: 계획 구조화
    ↓
마크다운 문서
    ↓
[MCP 서버]
    ├─ JSON 변환
    └─ Notion 저장
    ↓
Notion Database
    ├─ 구조화된 데이터
    ├─ 검색/필터 가능
    └─ 팀 협업
```

## 📚 문서 가이드

### 처음 시작하시나요?

1. **빠른 시작**: `thinking_box_mcp/QUICKSTART.md` (5분)
2. **통합 가이드**: `thinking_box_mcp/INTEGRATION_GUIDE.md`

### 상세 정보

- **Thinking Box 사용법**: `thinking_box/README.md`
- **MCP 서버 문서**: `thinking_box_mcp/README.md`
- **아키텍처**: `thinking_box_mcp/ARCHITECTURE.md`
- **설계 철학**: `thinking_box/DESIGN.md`

## 🔧 설정 확인

모든 설정이 제대로 되었는지 확인:

```bash
cd thinking_box_mcp
python check_setup.py
```

체크리스트:

- 디렉토리 구조
- 필수 파일
- 환경 변수
- 패키지 설치
- Notion 연결

## 🎓 학습 순서

1. **기본 사용** (thinking_box)

   - `python main.py` 실행
   - 3-Agent 분석 이해
   - 마크다운 출력 확인

2. **Notion 통합** (thinking_box_mcp)

   - Notion 설정
   - `python run.py` 실행
   - Database 확인

3. **고급 활용**
   - MCP 서버 설정
   - HTTP API 활용
   - 커스터마이징

## FAQ

**Q: 둘 중 뭘 써야 하나요?**
A: Notion 공유가 필요하면 `thinking_box_mcp/run.py`, 로컬 분석만이면 `thinking_box/main.py`

**Q: thinking_box만 사용해도 되나요?**
A: 네! 독립적으로 작동합니다. Notion이 필요 없으면 thinking_box만 사용하세요.

**Q: MCP 서버는 필수인가요?**
A: 아니요. `run.py`로 통합 실행하면 MCP 서버 없이도 Notion 저장 가능합니다.

**Q: Claude Desktop 연동은 어떻게 하나요?**
A: `thinking_box_mcp/README.md`의 "방식 1: MCP 서버" 섹션 참고

## 🛠️ 기술 스택

- **언어**: Python 3.8+
- **LLM**: Anthropic Claude (Sonnet 4.5)
- **Notion**: notion-client
- **MCP**: Anthropic MCP SDK
- **API**: FastAPI

## 📈 로드맵

- [x] 3-Agent 분석 시스템
- [x] Notion 자동 저장
- [x] MCP 서버 연동
- [x] HTTP REST API
- [ ] STT 통합
- [ ] 실시간 대시보드
- [ ] Slack/Discord 통합
- [ ] 멀티 워크스페이스

## 라이센스

MIT

---

**만든 사람**: 이상진
**버전**: 1.0.1
**최종 업데이트**: 2025-01-08

## 실제

Thinking Box는 현재는 사고 구조를 검증하는 프로토타입이지만,
유저별 사고 컨텍스트(Session)와 멀티 클라이언트(Web/App) 확장을 고려한
서비스형 구조로 설계되었습니다.

## Collaboration Rules (Preliminary Phase)

- main branch is stable
- feature work uses short-lived branches
- no force push to main
- keep commits small and descriptive
- discussion > code when unsure
