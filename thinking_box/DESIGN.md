# Thinking Box - 설계 원칙 및 확장 가이드

## 🎯 핵심 설계 원칙

### 1. 단순성 (Simplicity)
- **3개 에이전트만**: 각각 명확한 책임
- **선형 파이프라인**: Agent 1 → 2 → 3
- **공통 LLM 클라이언트**: 중복 제거

### 2. 모듈성 (Modularity)
```python
# 각 에이전트는 독립적
class Agent:
    def __init__(self, llm_client):
        self.llm = llm_client
    
    def process(self, input: str) -> str:
        # 단일 책임만 수행
        pass
```

### 3. 확장 가능성 (Extensibility)
새 에이전트 추가 시:
1. `agents/new_agent.py` 생성
2. `prompts/templates.py`에 프롬프트 추가
3. `main.py`에서 파이프라인에 연결

## 📊 각 에이전트 역할 상세

### Agent 1: 입력 정제 (Input Cleaning)
**목적**: 원본 → 구조화된 텍스트
- STT 노이즈 제거
- 필러워드 삭제 ("음", "저기", "그")
- 의미 단위로 세그먼트 분리
- 발화자 정보 보존

**입력**: 원본 회의록/대화
**출력**: 마크다운 세그먼트

### Agent 2: 아이디어 추출 (Idea Extraction)
**목적**: 대화 → 순위화된 아이디어
- 제안/가설/질문/관찰 분류
- 중요도 평가 (상/중/하)
- 참신함 평가
- 우선순위 재정렬

**입력**: 정제된 대화
**출력**: 순위화된 아이디어 리스트

### Agent 3: 계획 구조화 (Planning)
**목적**: 아이디어 → 실행 문서
- 문제 정의 추출
- 솔루션 방향 정리
- 액션 아이템 생성
- 열린 질문 식별

**입력**: 순위화된 아이디어
**출력**: 구조화된 계획 문서

## 🔧 확장 포인트

### 1. 프롬프트 튜닝
`prompts/templates.py`에서 각 에이전트의 프롬프트를 수정하여 출력 품질 개선

### 2. 중간 결과 저장
```python
# main.py에서
results = box.run(raw_input)
# 각 단계별 저장 가능
Path("step1_cleaned.md").write_text(results['cleaned_conversation'])
```

### 3. 병렬 처리 (선택적)
Agent 2와 3이 독립적이라면 병렬 실행 가능
```python
import asyncio
# 하지만 현재는 순차적 의존성이 있으므로 불필요
```

### 4. 피드백 루프 추가
```python
# Agent 3 이후 사용자 피드백 받아서 재처리
if user_feedback:
    revised = planning_agent.process(ideas, feedback=user_feedback)
```

## ⚠️ 하지 말아야 할 것

### ❌ 과도한 엔지니어링
- 복잡한 상태 관리
- 불필요한 캐싱 레이어
- 과도한 추상화

### ❌ 추가 에이전트
- "요약 에이전트"
- "검증 에이전트"
- "번역 에이전트"

→ **3개 에이전트로 충분합니다**

### ❌ UI/UX에 집중
- 웹 프론트엔드
- 실시간 스트리밍
- 화려한 시각화

→ **CLI로 충분합니다**

## 💡 실전 활용 팁

### 1. 회의록 처리
```bash
python main.py --input meeting_notes.txt --output insights.md
```

### 2. 브레인스토밍 정리
```bash
# 여러 아이디어 파일 순차 처리
for file in ideas/*.txt; do
    python main.py -i "$file" -o "output/$(basename $file .txt).md"
done
```

### 3. 프롬프트 A/B 테스트
`prompts/templates.py`에서 여러 버전 작성 후 성능 비교

## 🚀 다음 단계 (선택적)

1. **프롬프트 최적화**: 실제 사용 케이스에 맞게 조정
2. **평가 메트릭**: 출력 품질 측정 방법 개발
3. **에러 핸들링**: LLM 호출 실패 시 재시도 로직
4. **로깅**: 각 단계별 처리 시간 및 토큰 사용량 기록

## 📝 철학 리마인더

> "The value is in reasoning separation, not automation"

이 시스템의 핵심은:
- ✅ 사고 과정을 명확히 분리
- ✅ 각 단계의 출력을 검토 가능
- ✅ 인간의 사고를 지원

이것이 아닙니다:
- ❌ 완전 자동화
- ❌ SaaS 제품
- ❌ 복잡한 워크플로우 엔진
