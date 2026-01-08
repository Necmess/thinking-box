"""
Thinking Box - 메인 파이프라인

사용법:
    python main.py --input example_input.txt --output result.md
    또는
    python main.py  (대화형 모드)
"""
import argparse
from pathlib import Path
from datetime import datetime

from core.llm_client import LLMClient
from agents.input_agent import InputAgent
from agents.idea_agent import IdeaAgent
from agents.planning_agent import PlanningAgent


class ThinkingBox:
    """
    3단계 에이전트 파이프라인
    """
    
    def __init__(self):
        # 공통 LLM 클라이언트
        self.llm = LLMClient()
        
        # 3개 에이전트 초기화
        self.input_agent = InputAgent(self.llm)
        self.idea_agent = IdeaAgent(self.llm)
        self.planning_agent = PlanningAgent(self.llm)
    
    def run(self, raw_input: str) -> dict:
        """
        전체 파이프라인 실행
        
        Args:
            raw_input: 원본 대화/회의 텍스트
            
        Returns:
            각 단계의 출력을 담은 딕셔너리
        """
        print("=" * 60)
        print("🧠 Thinking Box 파이프라인 시작")
        print("=" * 60 + "\n")
        
        # Stage 1: 입력 정제
        cleaned = self.input_agent.process(raw_input)
        
        # Stage 2: 아이디어 추출
        ideas = self.idea_agent.process(cleaned)
        
        # Stage 3: 계획 구조화
        plan = self.planning_agent.process(ideas)
        
        print("=" * 60)
        print("✅ 파이프라인 완료!")
        print("=" * 60 + "\n")
        
        return {
            "cleaned_conversation": cleaned,
            "ranked_ideas": ideas,
            "planning_document": plan
        }
    
    def save_output(self, results: dict, output_path: str):
        """
        결과를 마크다운 파일로 저장
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"""# Thinking Box 출력 결과
생성 시간: {timestamp}

---

## 1단계: 정제된 대화

{results['cleaned_conversation']}

---

## 2단계: 순위화된 아이디어

{results['ranked_ideas']}

---

## 3단계: 구조화된 계획

{results['planning_document']}
"""
        
        Path(output_path).write_text(content, encoding='utf-8')
        print(f"📄 결과 저장 완료: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Thinking Box - 사고 지원 시스템")
    parser.add_argument("--input", "-i", help="입력 파일 경로")
    parser.add_argument("--output", "-o", default="output.md", help="출력 파일 경로")
    args = parser.parse_args()
    
    # 입력 읽기
    if args.input:
        raw_input = Path(args.input).read_text(encoding='utf-8')
    else:
        print("대화형 모드: 입력할 텍스트를 입력하세요 (빈 줄 두 번으로 종료):\n")
        lines = []
        empty_count = 0
        while True:
            line = input()
            if line == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                lines.append(line)
        raw_input = "\n".join(lines)
    
    # 파이프라인 실행
    box = ThinkingBox()
    results = box.run(raw_input)
    
    # 결과 저장
    box.save_output(results, args.output)
    
    # 최종 결과 미리보기
    print("\n" + "=" * 60)
    print("📋 최종 계획 문서 미리보기:")
    print("=" * 60)
    print(results['planning_document'])


if __name__ == "__main__":
    main()
