# Thinking Box - Cloud Deployment 🚀

**AI 기반 3단계 사고 분석 시스템** - Streamlit Cloud 배포 버전

Claude Sonnet 4 + Whisper base (한국어 최적화)

---

## ⚡️ 빠른 시작

```bash
# 1. 압축 해제
tar -xzf thinking-box-claude-deploy.tar.gz
cd thinking-box-claude-deploy

# 2. 기존 agents, prompts 복사
cp -r old_thinking_box/agents ./thinking_box/
cp -r old_thinking_box/prompts ./thinking_box/

# 3. GitHub 푸시
git init && git add . && git commit -m "Deploy"
git remote add origin <your-repo>
git push -u origin main

# 4. Streamlit Cloud 배포
# https://share.streamlit.io/
# → New app → 레포 선택 → Deploy!

# 5. API 키 설정
# Settings → Secrets → ANTHROPIC_API_KEY 추가
```

**배포 완료! 5분 소요**

---

## 📋 기술 스택

### LLM: Claude Sonnet 4

```
✅ 맥락 이해 탁월 (회의록 분석 최적)
✅ 긴 대화 처리 우수
✅ 한국어 품질 안정적
✅ 이미 프롬프트 최적화됨
```

### STT: Whisper base

```
✅ 크기: 74MB (경량)
✅ 한국어 정확도: ~85%
✅ 메모리: ~300MB
✅ Streamlit Cloud에서 작동
✅ 무료 (로컬 실행)
```

---

## 🎯 핵심 기능

- 🧠 **3단계 AI 분석**: 정제 → 아이디어 → 계획
- 📝 **텍스트 입력**: 회의록, 대화 직접 입력
- 🎤 **음성 입력**: 오디오 파일 STT (한국어/영어)
- 🌐 **웹 UI**: Streamlit 기반 인터페이스
- 💾 **결과 다운로드**: 마크다운 파일 저장

---

## 📦 구조

```
thinking-box-claude-deploy/
├── thinking_box/
│   ├── core/
│   │   └── llm_client.py         # Claude API
│   ├── agents/                    # ⚠️ 복사 필요
│   ├── prompts/                   # ⚠️ 복사 필요
│   ├── stt/
│   │   └── whisper_stt.py        # Whisper base
│   └── ui/
│       └── streamlit_app.py      # 클라우드 최적화
│
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
│
├── requirements.txt               # Anthropic + Whisper
├── README_DEPLOY.md               # 상세 배포 가이드
├── QUICKSTART_CLOUD.md            # 5분 빠른 시작
└── .gitignore
```

---

## 🚀 배포 가이드

### 상세 가이드

👉 [README_DEPLOY.md](README_DEPLOY.md)

### 빠른 시작 (5분)

👉 [QUICKSTART_CLOUD.md](QUICKSTART_CLOUD.md)

---

## 💰 비용

### Claude API

```
입력:  $3 / 1M tokens
출력:  $15 / 1M tokens

예상: 회의록 1개 = $0.01-0.05
```

### Streamlit Cloud

```
무료: Public apps
```

### Whisper

```
무료: 로컬 실행
```

**총 예상 비용: ~$1-5/월** (사용량에 따라)

---

## 🔧 로컬 개발

```bash
# 의존성 설치
pip install -r requirements.txt
brew install ffmpeg

# Secrets 설정
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# secrets.toml에 Claude API 키 입력

# 실행
streamlit run thinking_box/ui/streamlit_app.py
```

### 🧩 CLI 실행 (텍스트만)

```bash
cd thinking_box
export ANTHROPIC_API_KEY=your_api_key
python main.py --input example_input.txt --output result.md
```

Whisper STT와 Streamlit이 필요 없는 최소 실행 경로입니다.

---

## 📊 Claude vs 다른 LLM

| 특징            | Claude Sonnet 4 | GPT-4o       |
| --------------- | --------------- | ------------ |
| **회의록 분석** | ⭐️⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️⭐️ |
| **맥락 이해**   | ⭐️⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️⭐️ |
| **한국어**      | ⭐️⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️⭐️ |
| **긴 대화**     | ⭐️⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️    |
| **비용**        | ~$0.01/분석     | ~$0.01/분석  |

**결론**: 회의록 분석은 Claude가 더 적합! ✅

---

## ⚠️ 주의사항

### 필수 파일 복사

```bash
# agents와 prompts는 기존 프로젝트에서 복사!
cp -r old_thinking_box/agents ./thinking_box/
cp -r old_thinking_box/prompts ./thinking_box/
```

### Secrets 보안

```
.streamlit/secrets.toml을 Git에 커밋하지 마세요!
API 키는 Streamlit Cloud Secrets에만 저장!
```

### MCP 서버

```
이 배포 패키지는 thinking_box만 포함
thinking_box_mcp는 별도로 유지
```

---

## 🤝 기여

Issues와 Pull Requests 환영합니다!

---

## 📝 라이센스

MIT License

---

## 🔗 링크

- [Anthropic API](https://console.anthropic.com/)
- [Streamlit Cloud](https://streamlit.io/cloud)
- [Whisper](https://github.com/openai/whisper)

---

**Made with ❤️ | Thinking Box Team**
