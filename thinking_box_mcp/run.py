#!/usr/bin/env python3
"""
Thinking Box → Notion 원클릭 실행 스크립트

사용법:
    python run.py                          # 대화형 모드
    python run.py meeting_notes.txt        # 파일 입력
    python run.py meeting_notes.txt -o output.md  # 로컬 백업 포함
"""
import sys
from pathlib import Path

# 통합 시스템 임포트
from integrated_system import ThinkingBoxNotion


def main():
    """간단한 실행"""
    
    # 입력 파일 확인
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if not Path(input_file).exists():
            print(f"❌ 파일을 찾을 수 없습니다: {input_file}")
            sys.exit(1)
        
        raw_input = Path(input_file).read_text(encoding='utf-8')
        print(f"📂 입력 파일: {input_file}\n")
    else:
        # 대화형 모드
        print("=" * 70)
        print("🧠 Thinking Box → Notion 자동 저장 시스템")
        print("=" * 70)
        print("\n📝 회의록을 입력하세요 (빈 줄 두 번으로 종료):\n")
        
        lines = []
        empty_count = 0
        while True:
            try:
                line = input()
                if line == "":
                    empty_count += 1
                    if empty_count >= 2:
                        break
                else:
                    empty_count = 0
                    lines.append(line)
            except EOFError:
                break
        
        raw_input = "\n".join(lines)
        
        if not raw_input.strip():
            print("❌ 입력이 없습니다.")
            sys.exit(1)
    
    # 통합 시스템 실행
    try:
        system = ThinkingBoxNotion()
        results = system.process_and_save(raw_input)
        
        # 로컬 백업 (선택)
        if '-o' in sys.argv or '--output' in sys.argv:
            idx = sys.argv.index('-o') if '-o' in sys.argv else sys.argv.index('--output')
            output_file = sys.argv[idx + 1]
            system.save_local_output(results, output_path=output_file)
        
        # 성공!
        print("\n" + "🎉" * 35)
        print(f"\n✅ 완료! Notion에서 확인하세요:")
        print(f"🔗 {results['notion_result']['page_url']}\n")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
