#!/bin/bash
# Thinking Box + MCP 통합 설정 스크립트

echo "🔧 Thinking Box + Notion 통합 설정"
echo "===================================="
echo ""

# 1. 디렉토리 구조 확인
echo "📂 1단계: 프로젝트 구조 확인"

if [ ! -d "../thinking_box" ]; then
    echo "❌ thinking_box 폴더가 없습니다."
    echo ""
    echo "올바른 구조:"
    echo "  project/"
    echo "  ├── thinking_box/         # 기존 프로젝트"
    echo "  └── thinking_box_mcp/     # 이 폴더"
    echo ""
    echo "해결 방법:"
    echo "  1. thinking_box 폴더를 같은 위치에 배치"
    echo "  2. 또는 integrated_system.py의 경로 수정"
    exit 1
else
    echo "✅ thinking_box 폴더 발견"
fi

# 2. 의존성 설치
echo ""
echo "📦 2단계: 의존성 설치"
echo ""

# thinking_box 의존성
if [ -f "../thinking_box/requirements.txt" ]; then
    echo "Installing thinking_box dependencies..."
    pip install -r ../thinking_box/requirements.txt --quiet
    echo "✅ thinking_box 의존성 설치 완료"
else
    echo "⚠️  ../thinking_box/requirements.txt 없음"
fi

# thinking_box_mcp 의존성
if [ -f "requirements.txt" ]; then
    echo "Installing thinking_box_mcp dependencies..."
    pip install -r requirements.txt --quiet
    echo "✅ thinking_box_mcp 의존성 설치 완료"
fi

# 3. 환경 변수 확인
echo ""
echo "🔑 3단계: 환경 변수 확인"
echo ""

if [ ! -f ".env" ]; then
    echo "⚠️  .env 파일이 없습니다."
    echo "Creating .env from example..."
    cp .env.example .env
    echo ""
    echo "📝 다음 정보를 .env 파일에 입력하세요:"
    echo "   - NOTION_TOKEN"
    echo "   - NOTION_DATABASE_ID"
    echo "   - ANTHROPIC_API_KEY (thinking_box용)"
    echo ""
    echo "편집: nano .env"
    exit 1
else
    echo "✅ .env 파일 존재"
    
    # 필수 변수 확인
    source .env 2>/dev/null
    
    if [ -z "$NOTION_TOKEN" ]; then
        echo "❌ NOTION_TOKEN이 설정되지 않았습니다"
        exit 1
    fi
    
    if [ -z "$NOTION_DATABASE_ID" ]; then
        echo "❌ NOTION_DATABASE_ID가 설정되지 않았습니다"
        exit 1
    fi
    
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo "❌ ANTHROPIC_API_KEY가 설정되지 않았습니다"
        exit 1
    fi
    
    echo "✅ 모든 환경 변수 설정됨"
fi

# 4. Notion 연결 테스트
echo ""
echo "🔌 4단계: Notion 연결 테스트"
echo ""

python -c "
from notion_storage import NotionStorage
import sys

try:
    storage = NotionStorage()
    if storage.test_connection():
        print('✅ Notion 연결 성공!')
    else:
        print('❌ Notion 연결 실패')
        sys.exit(1)
except Exception as e:
    print(f'❌ 오류: {e}')
    sys.exit(1)
" || exit 1

# 5. 완료
echo ""
echo "===================================="
echo "✅ 설정 완료!"
echo "===================================="
echo ""
echo "🚀 사용법:"
echo "   python run.py                    # 대화형 모드"
echo "   python run.py meeting.txt        # 파일 입력"
echo ""
echo "📚 자세한 사용법: INTEGRATION_GUIDE.md"
echo ""
