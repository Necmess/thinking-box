# Thinking Box + Notion 완전 통합 가이드

## 🎯 개요

**두 프로젝트가 하나로 통합되었습니다!**

```
회의록 입력
    ↓
Thinking Box (3-agent 분석)
  - Agent 1: 정제
  - Agent 2: 아이디어 추출  
  - Agent 3: 계획 구조화
    ↓
자동 JSON 변환
    ↓
Notion Database 저장
    ↓
완료! 🎉
```

## 📂 프로젝트 구조

```
프로젝트_루트/
├── thinking_box/              # 기존 Thinking Box
│   ├── agents/
│   ├── core/
│   └── main.py
│
└── thinking_box_mcp/          # MCP 서버 + 통합
    ├── notion_storage.py      # Notion 연동
    ├── mcp_server.py          # MCP 서버
    ├── http_server.py         # HTTP API
    ├── integrated_system.py   # ⭐ 통합 시스템
    └── run.py                 # ⭐ 원클릭 실행
```

## 🚀 사용법

### 방법 1: 원클릭 실행 (가장 간단!)

```bash
cd thinking_box_mcp
python run.py
```

1. 프롬프트가 나오면 회의록 입력
2. 빈 줄 두 번 입력
3. 자동으로 분석 → Notion 저장!

### 방법 2: 파일 입력

```bash
python run.py ../thinking_box/example_input.txt
```

### 방법 3: 로컬 백업 포함

```bash
python run.py meeting.txt -o backup.md
```

## 🔄 전체 플로우 상세

### 1단계: Thinking Box 처리
```
원본 회의록 → Agent 1 → Agent 2 → Agent 3 → 마크다운 문서
```

### 2단계: 자동 변환
```python
마크다운 문서 → JSON 파싱
{
  "title": "추출된 제목",
  "idea_stage": "발산/수렴",
  "summary": "요약",
  "key_points": [...],
  "tasks": [...],
  "confidence": 0.87
}
```

### 3단계: Notion 저장
```
JSON → Notion API → Database에 페이지 생성
```

## 📊 실행 예시

```bash
$ python run.py

==================================================================
🧠 Thinking Box → Notion 자동 저장 시스템
==================================================================

📝 회의록을 입력하세요 (빈 줄 두 번으로 종료):

김팀장: 오늘은 신규 프로젝트 논의하겠습니다.
이과장: AI 챗봇 기능이 필요할 것 같아요.
박대리: 고객 응답 시간을 줄여야 합니다.


✅ Thinking Box + Notion 통합 시스템 초기화 완료

==================================================================
🧠 Thinking Box + Notion 통합 파이프라인 시작
==================================================================

📝 1단계: Thinking Box 에이전트 실행 중...

🔍 Agent 1: 입력 정제 중...
✓ 정제 완료

💡 Agent 2: 아이디어 추출 및 순위화 중...
✓ 아이디어 추출 완료

📋 Agent 3: 계획 구조화 중...
✓ 계획 문서 생성 완료

🔄 2단계: Notion 포맷으로 변환 중...

변환된 데이터:
  - 제목: AI 챗봇 기반 고객 응답 시스템 구축
  - 단계: 수렴
  - 핵심 포인트: 5개
  - 작업 항목: 7개

💾 3단계: Notion Database에 저장 중...

✅ Notion 저장 완료!
📄 페이지 URL: https://notion.so/abc123...

==================================================================
✅ 전체 파이프라인 완료!
==================================================================

🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉

✅ 완료! Notion에서 확인하세요:
🔗 https://notion.so/abc123...
```

## 🔧 프로그래밍 방식 사용

```python
from integrated_system import ThinkingBoxNotion

# 시스템 초기화
system = ThinkingBoxNotion()

# 회의록 처리 및 저장
results = system.process_and_save("""
여기에 회의록 내용...
""")

# 결과 확인
print(results['notion_result']['page_url'])

# 로컬 백업
system.save_local_output(results, "backup.md")
```

## 📋 Notion에 저장되는 정보

| 필드 | 내용 |
|------|------|
| **Title** | 자동 추출된 핵심 제목 |
| **Idea Stage** | "발산" 또는 "수렴" |
| **Summary** | 문제 정의 및 주요 내용 요약 |
| **Key Points** | 핵심 포인트 리스트 (최대 10개) |
| **Tasks** | 실행 단계 작업 항목 |
| **Confidence** | 분석 신뢰도 (0~1) |
| **Session ID** | 고유 세션 식별자 |
| **Created At** | 생성 시간 |

## 🎛️ 변환 로직

### 제목 추출
- "## 1. 문제 정의" 섹션에서 핵심 문제 추출
- 없으면 기본값 사용

### 아이디어 단계 판단
- "발산", "브레인스토밍" 키워드 → 발산
- 그 외 → 수렴

### 핵심 포인트 추출
- `- ` 로 시작하는 항목들 수집
- 체크박스 항목(`- [ ]`) 제외
- 최대 10개

### 작업 항목 추출
- "## 3. 실행 단계"의 체크박스 항목
- 최대 20개

### 신뢰도 계산
- 기본 점수: 0.5
- 실행 단계 존재: +0.2
- 열린 질문 존재: +0.1
- 아이디어 3개 이상: +0.1
- 작업 3개 이상: +0.1

## 🔍 문제 해결

### "Thinking Box 모듈을 찾을 수 없습니다"
```bash
# 프로젝트 구조 확인
project/
├── thinking_box/         # 여기 있어야 함
└── thinking_box_mcp/     # 여기서 실행
```

### "Notion 연결 실패"
`.env` 파일 확인:
```bash
NOTION_TOKEN=secret_...
NOTION_DATABASE_ID=...
```

### 변환이 이상함
`integrated_system.py`의 파싱 로직 커스터마이징 가능

## 🎨 커스터마이징

### 변환 로직 수정
```python
# integrated_system.py
class ThinkingBoxNotion:
    def _extract_title(self, plan: str) -> str:
        # 여기를 수정해서 제목 추출 방식 변경
        pass
    
    def _extract_key_points(self, plan: str) -> list:
        # 핵심 포인트 추출 로직 수정
        pass
```

### Notion 스키마 확장
```python
# notion_storage.py의 _build_properties() 수정
properties["Custom Field"] = {
    "rich_text": [{"text": {"content": "..."}}]
}
```

## 📈 다음 단계

1. **자동화**: cron으로 주기적 실행
2. **STT 통합**: 음성 → 텍스트 → Thinking Box
3. **알림**: Slack/Discord 통합
4. **대시보드**: 저장된 데이터 시각화

## 💡 팁

1. **긴 회의록**: 여러 세션으로 나누어 처리
2. **반복 실행**: 같은 회의록 여러 번 처리 가능 (새 페이지 생성됨)
3. **백업**: `-o` 옵션으로 로컬 마크다운 파일 보관

---

**이제 회의록을 입력하면 자동으로 분석 → Notion 저장까지 한 번에!** 🚀
