"""
Thinking Box + MCP 통합 시스템

원본 Thinking Box 3-agent 시스템의 출력을 자동으로 Notion에 저장
"""
import os
import sys
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

# Thinking Box 모듈 임포트 (원본 프로젝트에서)
sys.path.insert(0, str(Path(__file__).parent.parent / 'thinking_box'))
try:
    from core.llm_client import LLMClient
    from agents.input_agent import InputAgent
    from agents.idea_agent import IdeaAgent
    from agents.planning_agent import PlanningAgent
except ImportError:
    print("❌ Thinking Box 모듈을 찾을 수 없습니다.")
    print("thinking_box 폴더가 동일한 위치에 있는지 확인하세요.")
    sys.exit(1)

# MCP 서버 모듈 임포트
from notion_storage import NotionStorage

# 환경 변수 로드 (.env)
load_dotenv()


class ThinkingBoxNotion:
    """
    Thinking Box + Notion 통합 시스템
    
    회의록 → 3-agent 처리 → Notion 자동 저장
    """
    
    def __init__(self):
        """초기화"""
        # Thinking Box 에이전트
        self.llm = LLMClient()
        self.input_agent = InputAgent(self.llm)
        self.idea_agent = IdeaAgent(self.llm)
        self.planning_agent = PlanningAgent(self.llm)
        
        # Notion 클라이언트
        self.notion = NotionStorage()
        
        print("✅ Thinking Box + Notion 통합 시스템 초기화 완료")
    
    def process_and_save(self, raw_input: str, session_id: str = None) -> Dict[str, Any]:
        """
        전체 파이프라인 실행: 회의록 → 분석 → Notion 저장
        
        Args:
            raw_input: 원본 회의록/대화 텍스트
            session_id: 세션 ID (없으면 자동 생성)
            
        Returns:
            {
                'thinking_results': {...},  # Thinking Box 출력
                'notion_result': {...}      # Notion 저장 결과
            }
        """
        print("\n" + "=" * 70)
        print("🧠 Thinking Box + Notion 통합 파이프라인 시작")
        print("=" * 70 + "\n")
        
        # 세션 ID 생성
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # ===== 1단계: Thinking Box 처리 =====
        print("📝 1단계: Thinking Box 에이전트 실행 중...\n")
        
        # Agent 1: 입력 정제
        cleaned = self.input_agent.process(raw_input)
        
        # Agent 2: 아이디어 추출
        ideas = self.idea_agent.process(cleaned)
        
        # Agent 3: 계획 구조화
        plan = self.planning_agent.process(ideas)
        
        thinking_results = {
            'cleaned_conversation': cleaned,
            'ranked_ideas': ideas,
            'planning_document': plan
        }
        
        # ===== 2단계: JSON 포맷 변환 =====
        print("🔄 2단계: Notion 포맷으로 변환 중...\n")
        notion_data = self._convert_to_notion_format(
            session_id=session_id,
            thinking_results=thinking_results
        )
        
        print(f"변환된 데이터:")
        print(f"  - 제목: {notion_data['title']}")
        print(f"  - 단계: {notion_data['idea_stage']}")
        print(f"  - 핵심 포인트: {len(notion_data['key_points'])}개")
        print(f"  - 작업 항목: {len(notion_data['tasks'])}개")
        print()
        
        # ===== 3단계: Notion 저장 =====
        print("💾 3단계: Notion Database에 저장 중...\n")
        notion_result = self.notion.save_thinking_result(notion_data)
        
        print(f"✅ Notion 저장 완료!")
        print(f"📄 페이지 URL: {notion_result['page_url']}")
        print()
        
        print("=" * 70)
        print("✅ 전체 파이프라인 완료!")
        print("=" * 70 + "\n")
        
        return {
            'thinking_results': thinking_results,
            'notion_data': notion_data,
            'notion_result': notion_result
        }
    
    def _convert_to_notion_format(self, session_id: str, thinking_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Thinking Box 출력을 Notion 포맷으로 변환
        
        Thinking Box는 마크다운 문서를 출력하지만,
        Notion은 구조화된 JSON이 필요하므로 변환 작업 수행
        """
        plan = thinking_results['planning_document']
        ideas = thinking_results['ranked_ideas']
        
        # 간단한 파싱 (실제로는 더 정교한 파싱 필요)
        # 제목 추출
        title = self._extract_title(plan)
        
        # 아이디어 단계 결정 (ideas 내용 기반)
        idea_stage = self._determine_stage(ideas)
        
        # 요약 추출
        summary = self._extract_summary(plan)
        
        # 핵심 포인트 추출
        key_points = self._extract_key_points(plan)
        
        # 작업 항목 추출
        tasks = self._extract_tasks(plan)
        
        # 신뢰도 계산 (간단한 휴리스틱)
        confidence = self._calculate_confidence(plan, ideas)
        
        return {
            "session_id": session_id,
            "idea_stage": idea_stage,
            "title": title,
            "summary": summary,
            "key_points": key_points,
            "tasks": tasks,
            "confidence": confidence
        }
    
    def _extract_title(self, plan: str) -> str:
        """계획 문서에서 제목 추출"""
        lines = plan.split('\n')
        for line in lines:
            if line.startswith('## 1. 문제 정의'):
                # 다음 줄부터 제목 찾기
                idx = lines.index(line)
                for i in range(idx + 1, min(idx + 5, len(lines))):
                    if lines[i].strip() and not lines[i].startswith('#'):
                        return lines[i].replace('**핵심 문제**:', '').strip()[:100]
        
        return "Thinking Box 분석 결과"
    
    def _determine_stage(self, ideas: str) -> str:
        """아이디어 단계 결정"""
        # 간단한 키워드 기반 분류
        if '발산' in ideas or '브레인스토밍' in ideas or '다양한' in ideas:
            return '발산'
        else:
            return '수렴'
    
    def _extract_summary(self, plan: str) -> str:
        """요약 추출"""
        lines = plan.split('\n')
        summary_parts = []
        
        in_problem_section = False
        for line in lines:
            if '## 1. 문제 정의' in line:
                in_problem_section = True
            elif line.startswith('## 2.'):
                break
            elif in_problem_section and line.strip() and not line.startswith('#'):
                summary_parts.append(line.strip())
        
        summary = ' '.join(summary_parts)[:500]  # 500자 제한
        return summary if summary else "Thinking Box 에이전트가 분석한 사고 구조화 결과입니다."
    
    def _extract_key_points(self, plan: str) -> list:
        """핵심 포인트 추출"""
        key_points = []
        lines = plan.split('\n')
        
        for line in lines:
            # - 로 시작하는 항목 추출
            if line.strip().startswith('- ') and not line.strip().startswith('- [ ]'):
                point = line.strip()[2:].strip()[:100]  # 100자 제한
                if point and point not in key_points:
                    key_points.append(point)
        
        return key_points[:10]  # 최대 10개
    
    def _extract_tasks(self, plan: str) -> list:
        """작업 항목 추출"""
        tasks = []
        lines = plan.split('\n')
        
        in_action_section = False
        for line in lines:
            if '## 3. 실행 단계' in line:
                in_action_section = True
            elif line.startswith('## 4.'):
                break
            elif in_action_section and line.strip().startswith('- [ ]'):
                task_text = line.strip()[5:].strip()
                # 담당자 추출 시도
                if ':' in task_text or '(' in task_text:
                    owner = "담당자 미정"
                    task = task_text
                else:
                    owner = "팀"
                    task = task_text
                
                tasks.append({
                    "owner": owner,
                    "task": task[:200]  # 200자 제한
                })
        
        return tasks[:20]  # 최대 20개
    
    def _calculate_confidence(self, plan: str, ideas: str) -> float:
        """신뢰도 계산 (간단한 휴리스틱)"""
        # 계획의 구조적 완성도 기반
        score = 0.5  # 기본 점수
        
        # 실행 단계가 있으면 +0.2
        if '## 3. 실행 단계' in plan:
            score += 0.2
        
        # 열린 질문이 있으면 +0.1
        if '## 4. 열린 질문' in plan:
            score += 0.1
        
        # 아이디어가 3개 이상이면 +0.1
        if ideas.count('**[') >= 3:
            score += 0.1
        
        # 작업이 3개 이상이면 +0.1
        if plan.count('- [ ]') >= 3:
            score += 0.1
        
        return min(score, 1.0)
    
    def save_local_output(self, results: Dict[str, Any], output_path: str = None):
        """
        결과를 로컬 파일로도 저장 (백업용)
        """
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"thinking_box_output_{timestamp}.md"
        
        content = f"""# Thinking Box + Notion 통합 결과
생성 시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
세션 ID: {results['notion_data']['session_id']}
Notion 페이지: {results['notion_result']['page_url']}

---

## 정제된 대화
{results['thinking_results']['cleaned_conversation']}

---

## 순위화된 아이디어
{results['thinking_results']['ranked_ideas']}

---

## 구조화된 계획
{results['thinking_results']['planning_document']}

---

## Notion 저장 정보
- 제목: {results['notion_data']['title']}
- 단계: {results['notion_data']['idea_stage']}
- 신뢰도: {results['notion_data']['confidence']}
- 페이지 ID: {results['notion_result']['page_id']}
"""
        
        Path(output_path).write_text(content, encoding='utf-8')
        print(f"📄 로컬 백업 저장: {output_path}")


def main():
    """메인 실행"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Thinking Box + Notion 통합 시스템")
    parser.add_argument("--input", "-i", help="입력 파일 경로")
    parser.add_argument("--output", "-o", help="로컬 백업 파일 경로 (선택)")
    parser.add_argument("--session-id", "-s", help="세션 ID (선택)")
    args = parser.parse_args()
    
    # 입력 읽기
    if args.input:
        raw_input = Path(args.input).read_text(encoding='utf-8')
    else:
        print("📝 대화형 모드: 회의록을 입력하세요 (빈 줄 두 번으로 종료):\n")
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
    
    # 통합 시스템 실행
    system = ThinkingBoxNotion()
    results = system.process_and_save(raw_input, session_id=args.session_id)
    
    # 로컬 백업 저장
    system.save_local_output(results, output_path=args.output)
    
    # 최종 결과 출력
    print("\n" + "=" * 70)
    print("📊 최종 결과")
    print("=" * 70)
    print(f"✅ Notion 페이지: {results['notion_result']['page_url']}")
    print(f"📄 로컬 백업: {args.output if args.output else '저장 안 함'}")
    print()


if __name__ == "__main__":
    main()
