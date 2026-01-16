"""
Thinking Box - Streamlit Cloud Deployment
Claude API + Whisper base 버전

최적화:
- Claude Sonnet 4 (맥락 이해 우수)
- Whisper base (한국어 정확도 85%)
- Caching for performance
- Korean/English support
"""
import streamlit as st
from pathlib import Path
import tempfile
import sys
import uuid
import os
from dotenv import load_dotenv

# 로컬 실행 시 .env 로드 (Streamlit Cloud에서는 Secrets 사용)
# 루트(.env) 또는 MCP(.env) 경로 탐색
DOTENV_PATH = Path(__file__).resolve().parents[2] / ".env"
MCP_ENV_PATH = Path(__file__).resolve().parents[2] / "thinking_box_mcp" / ".env"
for candidate in (DOTENV_PATH, MCP_ENV_PATH):
    if candidate.exists():
        load_dotenv(dotenv_path=candidate)
        break
load_dotenv(dotenv_path=DOTENV_PATH if DOTENV_PATH.exists() else None)

# Add parent directory to path
if __name__ == "__main__":
    package_dir = Path(__file__).resolve().parents[1]  # .../thinking_box/thinking_box
    repo_root = Path(__file__).resolve().parents[2]     # .../thinking_box
    sys.path.insert(0, str(package_dir))
    sys.path.insert(0, str(repo_root))

from thinking_box import ThinkingBox
from thinking_box.stt import WhisperSTT
from thinking_box_mcp.notion_storage import NotionStorage
from typing import Dict, Any


# Page config
st.set_page_config(
    page_title="Thinking Box - AI 사고 분석",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache models to avoid reloading
@st.cache_resource
def load_thinking_box():
    """캐시된 Thinking Box (한 번만 로딩)"""
    try:
        return ThinkingBox()
    except Exception as e:
        st.error(f"❌ Thinking Box 초기화 실패: {e}")
        st.info("💡 Claude API 키가 설정되었는지 확인하세요 (Settings → Secrets)")
        return None

@st.cache_resource
def load_stt():
    """캐시된 STT 모델 (한 번만 로딩)"""
    try:
        with st.spinner("🎤 STT 모델 로딩 중... (최초 1회, ~15초)"):
            return WhisperSTT(model_name="base")
    except Exception as e:
        st.error(f"❌ STT 모델 로딩 실패: {e}")
        return None

def load_notion_storage():
    """캐시된 Notion 클라이언트"""
    try:
        return NotionStorage()
    except Exception as e:
        st.error(f"❌ Notion 클라이언트 초기화 실패: {e}")
        st.info("💡 NOTION_TOKEN, NOTION_DATABASE_ID 환경 변수를 확인하세요.")
        return None


def _convert_to_notion_format(session_id: str, cleaned: str, ideas: str, plan: str) -> Dict[str, Any]:
    """Thinking Box 결과를 Notion 저장 포맷으로 단순 변환"""
    def extract_title(plan_text: str) -> str:
        lines = plan_text.split("\n")
        for idx, line in enumerate(lines):
            if line.startswith("## 1. 문제 정의"):
                for i in range(idx + 1, min(idx + 5, len(lines))):
                    if lines[i].strip() and not lines[i].startswith("#"):
                        return lines[i].replace("**핵심 문제**:", "").strip()[:100]
        return "Thinking Box 분석 결과"

    def determine_stage(ideas_text: str) -> str:
        return "발산" if ("발산" in ideas_text or "브레인스토밍" in ideas_text or "다양한" in ideas_text) else "수렴"

    def extract_summary(plan_text: str) -> str:
        lines = plan_text.split("\n")
        summary_parts = []
        in_problem = False
        for line in lines:
            if "## 1. 문제 정의" in line:
                in_problem = True
            elif line.startswith("## 2."):
                break
            elif in_problem and line.strip() and not line.startswith("#"):
                summary_parts.append(line.strip())
        summary = " ".join(summary_parts)[:500]
        return summary or "Thinking Box 에이전트가 분석한 사고 구조화 결과입니다."

    def extract_key_points(plan_text: str):
        key_points = []
        for line in plan_text.split("\n"):
            if line.strip().startswith("- ") and not line.strip().startswith("- [ ]"):
                point = line.strip()[2:].strip()[:100]
                if point and point not in key_points:
                    key_points.append(point)
        return key_points[:10]

    def extract_tasks(plan_text: str):
        tasks = []
        lines = plan_text.split("\n")
        in_action = False
        for line in lines:
            if "## 3. 실행 단계" in line:
                in_action = True
            elif line.startswith("## 4."):
                break
            elif in_action and line.strip().startswith("- [ ]"):
                task_text = line.strip()[5:].strip()
                tasks.append({"owner": "팀", "task": task_text[:200]})
        return tasks[:20]

    def calculate_confidence(plan_text: str, ideas_text: str) -> float:
        score = 0.5
        if "## 3. 실행 단계" in plan_text:
            score += 0.2
        if "## 4. 열린 질문" in plan_text:
            score += 0.1
        if ideas_text.count("**[") >= 3:
            score += 0.1
        if plan_text.count("- [ ]") >= 3:
            score += 0.1
        return min(score, 1.0)

    return {
        "session_id": session_id,
        "idea_stage": determine_stage(ideas),
        "title": extract_title(plan),
        "summary": extract_summary(plan),
        "key_points": extract_key_points(plan),
        "tasks": extract_tasks(plan),
        "confidence": calculate_confidence(plan, ideas),
    }


# Title and description
st.title("🧠 Thinking Box")
st.markdown("""
**AI 기반 3단계 사고 분석 시스템**

회의록이나 대화를 구조화된 계획으로 변환합니다.
""")

# Sidebar
with st.sidebar:
    st.header("⚙️ 설정")
    
    # Input method
    input_mode = st.radio(
        "입력 방식",
        ["📝 텍스트", "🎤 음성 (STT)"],
        help="텍스트를 직접 입력하거나 음성 파일을 업로드하세요"
    )
    
    # Language for STT
    if "음성" in input_mode:
        st.markdown("---")
        language_options = {
            "자동 감지": None,
            "한국어": "ko",
            "English": "en"
        }
        language = st.selectbox(
            "오디오 언어",
            list(language_options.keys())
        )
        language_code = language_options[language]
    else:
        language_code = None
    
    # Info
    st.markdown("---")
    st.info("""
    **3단계 분석:**
    1. 입력 정제
    2. 아이디어 추출
    3. 계획 구조화
    
    **사용 모델:**
    - LLM: Claude Sonnet 4
    - STT: Whisper base (85% 정확도)
    """)

    # Env status
    notion_ok = bool(os.getenv("NOTION_TOKEN")) and bool(os.getenv("NOTION_DATABASE_ID"))
    st.markdown("---")
    st.caption(f"Notion env 상태: {'✅' if notion_ok else '❌'} (토큰/DB ID)")
    
    # API status check
    if st.button("🔌 API 연결 확인"):
        box = load_thinking_box()
        if box:
            st.success("✅ Claude API 연결됨")
        else:
            st.error("❌ API 키 확인 필요")

st.markdown("---")

# Main content
raw_input = None

if "텍스트" in input_mode:
    st.subheader("📝 텍스트 입력")
    raw_input = st.text_area(
        "회의록이나 대화 내용을 입력하세요",
        height=250,
        placeholder="예: 오늘 팀 회의에서 신규 프로젝트에 대해 논의했습니다...",
        help="한국어와 영어 모두 지원합니다"
    )

else:  # 음성 입력
    st.subheader("🎤 음성 입력 (Speech-to-Text)")
    
    st.info("""
    📌 **지원 형식**: .wav, .mp3, .m4a  
    💡 **팁**: 짧은 오디오 (<5분) 권장  
    🎯 **정확도**: base 모델 사용 (~85% 한국어)
    """)
    
    uploaded_file = st.file_uploader(
        "오디오 파일 업로드",
        type=["wav", "mp3", "m4a", "ogg"],
        help="음성 파일을 선택하세요"
    )
    
    if uploaded_file:
        # Save to temp file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=Path(uploaded_file.name).suffix
        ) as tmp:
            tmp.write(uploaded_file.read())
            audio_path = tmp.name
        
        # Show audio player
        st.audio(audio_path)
        
        # Transcribe button
        if st.button("🔊 음성 인식 시작", type="primary"):
            stt = load_stt()
            
            if stt is None:
                st.error("❌ STT 모델을 로드할 수 없습니다")
            else:
                with st.spinner("음성을 텍스트로 변환 중... (base 모델)"):
                    try:
                        raw_input = stt.transcribe(audio_path, language=language_code)
                        st.success("✅ 음성 인식 완료!")
                        
                        with st.expander("📄 인식된 텍스트 보기"):
                            st.text_area(
                                "Transcript:",
                                raw_input,
                                height=150,
                                disabled=True
                            )
                        
                        st.session_state.transcript = raw_input
                        
                    except Exception as e:
                        st.error(f"❌ 음성 인식 실패: {e}")
                        raw_input = None

# Use transcript from session if available
if 'transcript' in st.session_state and raw_input is None:
    raw_input = st.session_state.transcript

st.markdown("---")

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    run_button = st.button(
        "▶️ 분석 시작",
        type="primary",
        disabled=not raw_input,
        use_container_width=True
    )

with col2:
    if st.button("🗑️ 초기화", use_container_width=True):
        if 'transcript' in st.session_state:
            del st.session_state.transcript
        st.rerun()

with col3:
    if st.button("ℹ️ 도움말", use_container_width=True):
        st.info("""
        **사용 방법:**
        1. 입력 방식 선택 (텍스트/음성)
        2. 내용 입력 또는 파일 업로드
        3. "분석 시작" 클릭
        
        **문제 해결:**
        - API 키: Streamlit Cloud Settings → Secrets
        - 음성 인식 실패: 파일 형식 확인
        - base 모델: 첫 로딩 ~15초 소요
        """)

# Processing
if run_button:
    if not raw_input:
        st.warning("⚠️ 입력을 먼저 제공해주세요")
    else:
        # Load Thinking Box
        box = load_thinking_box()
        
        if box is None:
            st.error("❌ Thinking Box를 초기화할 수 없습니다. API 키를 확인하세요.")
            st.stop()
        
        # Output container
        output_container = st.container()
        
        with output_container:
            st.markdown("---")
            st.subheader("📊 분석 진행 중...")
            
            # Progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Stage 1: Cleaning
                status_text.info("🔍 1/3: 입력 정제 중... (Claude Sonnet 4)")
                progress_bar.progress(10)
                
                cleaned = box.input_agent.process(raw_input)
                progress_bar.progress(33)
                
                # Stage 2: Ideas
                status_text.info("💡 2/3: 아이디어 추출 중... (Claude Sonnet 4)")
                progress_bar.progress(40)
                
                ideas = box.idea_agent.process(cleaned)
                progress_bar.progress(66)
                
                # Stage 3: Planning
                status_text.info("📋 3/3: 계획 구조화 중... (Claude Sonnet 4)")
                progress_bar.progress(75)
                
                plan = box.planning_agent.process(ideas)
                progress_bar.progress(100)
                
                status_text.success("✅ 분석 완료!")
                # Store results in session for reuse (Notion 저장 버튼 등)
                st.session_state.analysis = {
                    "cleaned": cleaned,
                    "ideas": ideas,
                    "plan": plan
                }
                
            except Exception as e:
                st.error(f"❌ 처리 중 오류 발생:")
                st.exception(e)
                
                if "API key" in str(e) or "authentication" in str(e).lower():
                    st.info("""
                    💡 **Claude API 키 설정 방법:**
                    
                    Streamlit Cloud:
                    1. 앱 대시보드 → Settings
                    2. Secrets → Edit
                    3. 추가: `ANTHROPIC_API_KEY = "sk-ant-..."`
                    
                    로컬:
                    1. `.streamlit/secrets.toml` 파일 생성
                    2. 추가: `ANTHROPIC_API_KEY = "sk-ant-..."`
                    """)

# Persisted results display (works after rerun, e.g., Notion 버튼 클릭)
if 'analysis' in st.session_state:
    data = st.session_state['analysis']
    cleaned = data["cleaned"]
    ideas = data["ideas"]
    plan = data["plan"]

    st.markdown("---")
    st.subheader("📄 분석 결과")
    
    tab1, tab2, tab3 = st.tabs([
        "📋 최종 계획",
        "💡 아이디어",
        "🔍 정제된 입력"
    ])
    
    with tab1:
        st.markdown("### 구조화된 계획")
        st.markdown(plan)
        
        st.download_button(
            label="💾 다운로드 (.md)",
            data=plan,
            file_name="thinking_box_plan.md",
            mime="text/markdown"
        )
    
    with tab2:
        st.markdown("### 추출된 아이디어")
        st.text(ideas)
    
    with tab3:
        st.markdown("### 정제된 대화")
        st.text(cleaned)
    
    st.markdown("---")
    st.subheader("📥 Notion 저장")
    notion_btn = st.button("💾 Notion에 저장", type="primary", use_container_width=True)
    
    if notion_btn:
        notion_client = load_notion_storage()
        if notion_client is None:
            st.error("Notion 클라이언트 초기화에 실패했습니다.")
        else:
            with st.spinner("Notion에 저장 중..."):
                try:
                    session_id = str(uuid.uuid4())
                    notion_payload = _convert_to_notion_format(
                        session_id=session_id,
                        cleaned=cleaned,
                        ideas=ideas,
                        plan=plan,
                    )
                    notion_result = notion_client.save_thinking_result(notion_payload)
                    st.success("✅ Notion 저장 완료!")
                    st.markdown(f"[Notion 페이지 바로가기]({notion_result['page_url']})")
                    st.caption(f"Session ID: {session_id}")
                except Exception as e:
                    st.error(f"❌ Notion 저장 실패: {e}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Thinking Box | Claude Sonnet 4 + Whisper base | "
    "<a href='https://github.com/yourusername/thinking-box'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True
)
