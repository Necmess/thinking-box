# Thinking Box 프로젝트

회의록/대화를 3단계로 분석하고 Notion에 자동 저장하는 멀티 에이전트 시스템

## 📂 프로젝트 구성

### 📁 [thinking_box/](./thinking_box)
**핵심 분석 엔진** - 3-Agent 사고 지원 시스템

- 3단계 분석: 정제 → 아이디어 추출 → 계획 구조화
- 마크다운 출력
- 독립 실행 가능

```bash
cd thinking_box
python main.py --input example_input.txt
```

[📖 상세 문서](./thinking_box/README.md)

---

### 📁 [thinking_box_mcp/](./thinking_box_mcp)
**MCP 서버 & Notion 통합** - 자동 저장 시스템

- Notion Database 자동 저장
- MCP 서버 (Claude Desktop 연동)
- HTTP REST API
- Thinking Box와 완전 통합

```bash
cd thinking_box_mcp
python run.py
```

[📖 상세 문서](./thinking_box_mcp/README.md) | [🚀 빠른 시작](./thinking_box_mcp/QUICKSTART.md)

---

## 🚀 빠른 시작

### 1. 설치
```bash
# Thinking Box 의존성
cd thinking_box
pip install -r requirements.txt

# MCP 서버 의존성
cd ../thinking_box_mcp
pip install -r requirements.txt
```

### 2. 환경 설정

**thinking_box/.env**:
```
ANTHROPIC_API_KEY=your_api_key
```

**thinking_box_mcp/.env**:
```
ANTHROPIC_API_KEY=your_api_key
NOTION_TOKEN=secret_...
NOTION_DATABASE_ID=...
```

### 3. 실행

#### 옵션 A: 기본 분석 (마크다운만)
```bash
cd thinking_box
python main.py --input example_input.txt
```

#### 옵션 B: Notion 자동 저장 ⭐️
```bash
cd thinking_box_mcp
python run.py
```

---

## 💡 사용 시나리오

| 상황 | 사용 방법 | 설명 |
|------|----------|------|
| 빠른 분석 | `thinking_box/main.py` | 로컬 마크다운 생성 |
| Notion 공유 | `thinking_box_mcp/run.py` | 자동 저장 + 팀 공유 |
| API 서버 | `thinking_box_mcp/http_server.py` | 외부 시스템 연동 |
| Claude Desktop | MCP 설정 | 직접 연동 |

---

## 🎯 핵심 기능

### Thinking Box (핵심 엔진)
- ✅ Agent 1: 노이즈 제거 & 구조화
- ✅ Agent 2: 아이디어 추출 & 순위화
- ✅ Agent 3: 실행 계획 구조화
- ✅ 마크다운 출력

### MCP 서버 (통합 & 저장)
- ✅ Thinking Box 자동 실행
- ✅ JSON 자동 변환
- ✅ Notion 자동 저장
- ✅ HTTP REST API
- ✅ MCP 프로토콜 (Claude Desktop)

---

## 📊 데이터 플로우

```
원본 회의록
    ↓
[thinking_box]
  - Agent 1: 정제
  - Agent 2: 아이디어
  - Agent 3: 계획
    ↓
마크다운 문서
    ↓
[thinking_box_mcp]
  - JSON 변환
  - Notion 저장
    ↓
Notion Database
```

---

## 📚 문서

- **Thinking Box**: [thinking_box/README.md](./thinking_box/README.md)
- **MCP 서버**: [thinking_box_mcp/README.md](./thinking_box_mcp/README.md)
- **빠른 시작**: [thinking_box_mcp/QUICKSTART.md](./thinking_box_mcp/QUICKSTART.md)
- **통합 가이드**: [thinking_box_mcp/INTEGRATION_GUIDE.md](./thinking_box_mcp/INTEGRATION_GUIDE.md)
- **아키텍처**: [thinking_box_mcp/ARCHITECTURE.md](./thinking_box_mcp/ARCHITECTURE.md)

---

## 🤝 기여

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

## 📝 라이센스

MIT License

---

**Made with ❤️ by Thinking Box Team**
