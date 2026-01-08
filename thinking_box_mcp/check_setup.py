#!/usr/bin/env python3
"""
통합 시스템 설정 확인 스크립트

사용법: python check_setup.py
"""
import sys
from pathlib import Path


def check_setup():
    """설정 상태 확인"""
    print("🔍 Thinking Box + MCP 통합 시스템 설정 확인\n")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # 1. 디렉토리 구조 확인
    print("\n📂 1. 디렉토리 구조")
    print("-" * 60)
    
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    thinking_box_dir = parent_dir / 'thinking_box'
    
    if thinking_box_dir.exists():
        print(f"✅ thinking_box 폴더 발견: {thinking_box_dir}")
    else:
        print(f"❌ thinking_box 폴더 없음: {thinking_box_dir}")
        errors.append("thinking_box 폴더가 필요합니다")
    
    # 2. 필수 파일 확인
    print("\n📄 2. 필수 파일 확인")
    print("-" * 60)
    
    # thinking_box 파일들
    tb_files = [
        'agents/__init__.py',
        'agents/input_agent.py',
        'agents/idea_agent.py',
        'agents/planning_agent.py',
        'core/llm_client.py',
        'prompts/templates.py'
    ]
    
    for file in tb_files:
        file_path = thinking_box_dir / file
        if file_path.exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            errors.append(f"thinking_box/{file} 파일이 없습니다")
    
    # thinking_box_mcp 파일들
    mcp_files = [
        'notion_storage.py',
        'integrated_system.py',
        'run.py'
    ]
    
    print()
    for file in mcp_files:
        file_path = current_dir / file
        if file_path.exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            errors.append(f"{file} 파일이 없습니다")
    
    # 3. 환경 변수 확인
    print("\n🔑 3. 환경 변수 확인")
    print("-" * 60)
    
    env_file = current_dir / '.env'
    if not env_file.exists():
        print("❌ .env 파일이 없습니다")
        errors.append(".env 파일을 생성해야 합니다 (cp .env.example .env)")
    else:
        print("✅ .env 파일 존재")
        
        # .env 내용 확인
        import os
        from dotenv import load_dotenv
        
        try:
            load_dotenv(env_file)
            
            required_vars = [
                'NOTION_TOKEN',
                'NOTION_DATABASE_ID',
                'ANTHROPIC_API_KEY'
            ]
            
            for var in required_vars:
                value = os.getenv(var)
                if value and value != f"your_{var.lower()}_here":
                    print(f"✅ {var} 설정됨")
                else:
                    print(f"❌ {var} 미설정")
                    errors.append(f"{var}를 .env 파일에 설정해야 합니다")
        except Exception as e:
            print(f"⚠️  .env 파일 로드 실패: {e}")
            warnings.append("python-dotenv 설치 필요: pip install python-dotenv")
    
    # 4. 패키지 확인
    print("\n📦 4. 필수 패키지 확인")
    print("-" * 60)
    
    packages = [
        ('anthropic', 'Thinking Box용'),
        ('notion_client', 'Notion 연동용'),
        ('fastapi', 'HTTP API용'),
        ('dotenv', '환경 변수용')
    ]
    
    for pkg, purpose in packages:
        try:
            if pkg == 'dotenv':
                __import__('dotenv')
            else:
                __import__(pkg)
            print(f"✅ {pkg:20s} - {purpose}")
        except ImportError:
            print(f"❌ {pkg:20s} - {purpose}")
            warnings.append(f"{pkg} 설치 필요: pip install {pkg}")
    
    # 5. Notion 연결 테스트
    print("\n🔌 5. Notion 연결 테스트")
    print("-" * 60)
    
    try:
        from notion_storage import NotionStorage
        storage = NotionStorage()
        if storage.test_connection():
            print("✅ Notion 연결 성공!")
        else:
            print("❌ Notion 연결 실패")
            errors.append("Notion 토큰/DB ID를 확인하세요")
    except Exception as e:
        print(f"❌ Notion 연결 테스트 실패: {e}")
        errors.append(str(e))
    
    # 최종 결과
    print("\n" + "=" * 60)
    print("📊 최종 결과")
    print("=" * 60)
    
    if not errors and not warnings:
        print("\n✅ 모든 설정이 완료되었습니다!")
        print("\n🚀 사용법:")
        print("   python run.py")
        return True
    else:
        if errors:
            print(f"\n❌ {len(errors)}개의 오류:")
            for i, error in enumerate(errors, 1):
                print(f"   {i}. {error}")
        
        if warnings:
            print(f"\n⚠️  {len(warnings)}개의 경고:")
            for i, warning in enumerate(warnings, 1):
                print(f"   {i}. {warning}")
        
        print("\n💡 해결 방법:")
        print("   1. .env 파일 생성: cp .env.example .env")
        print("   2. 의존성 설치: pip install -r requirements.txt")
        print("   3. Notion 토큰/DB ID 입력")
        
        return False


if __name__ == "__main__":
    success = check_setup()
    sys.exit(0 if success else 1)
