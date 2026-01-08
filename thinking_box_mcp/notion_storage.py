"""
Notion Database 연동 모듈

Thinking Box 에이전트 출력을 Notion Database에 저장
"""
import os
from typing import Dict, Any, List
from datetime import datetime
from notion_client import Client


class NotionStorage:
    """
    Notion Database에 Thinking Box 결과를 저장하는 클라이언트
    """
    
    def __init__(self, token: str = None, database_id: str = None):
        """
        Args:
            token: Notion Integration Token
            database_id: 저장할 Database ID
        """
        self.token = token or os.getenv("NOTION_TOKEN")
        self.database_id = database_id or os.getenv("NOTION_DATABASE_ID")
        
        if not self.token:
            raise ValueError("NOTION_TOKEN이 필요합니다")
        if not self.database_id:
            raise ValueError("NOTION_DATABASE_ID가 필요합니다")
        
        self.client = Client(auth=self.token)
    
    def save_thinking_result(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Thinking Box 결과를 Notion Database에 저장
        
        Args:
            data: 에이전트 출력 JSON
            {
                "session_id": "uuid",
                "idea_stage": "발산 | 수렴",
                "title": "아이디어 제목",
                "summary": "요약",
                "key_points": ["핵심1", "핵심2"],
                "tasks": [
                    {"owner": "FE", "task": "와이어프레임"},
                    {"owner": "BE", "task": "API 설계"}
                ],
                "confidence": 0.87
            }
        
        Returns:
            생성된 Notion 페이지 정보
        """
        # Notion API 포맷으로 변환
        properties = self._build_properties(data)
        
        # Notion Database에 페이지 생성
        response = self.client.pages.create(
            parent={"database_id": self.database_id},
            properties=properties
        )
        
        return {
            "success": True,
            "page_id": response["id"],
            "page_url": response["url"],
            "created_time": response["created_time"]
        }
    
    def _build_properties(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        에이전트 데이터를 Notion Properties 포맷으로 변환
        """
        properties = {}
        
        # Title (title)
        if "title" in data:
            properties["Title"] = {
                "title": [
                    {
                        "text": {
                            "content": data["title"]
                        }
                    }
                ]
            }
        
        # Idea Stage (select)
        if "idea_stage" in data:
            properties["Idea Stage"] = {
                "select": {
                    "name": data["idea_stage"]
                }
            }
        
        # Summary (rich_text)
        if "summary" in data:
            properties["Summary"] = {
                "rich_text": [
                    {
                        "text": {
                            "content": data["summary"][:2000]  # Notion 제한
                        }
                    }
                ]
            }
        
        # Key Points (multi_select)
        if "key_points" in data and isinstance(data["key_points"], list):
            properties["Key Points"] = {
                "multi_select": [
                    {"name": point[:100]} for point in data["key_points"][:10]
                ]
            }
        
        # Tasks (rich_text) - JSON 문자열로 저장
        if "tasks" in data and isinstance(data["tasks"], list):
            tasks_text = "\n".join([
                f"[{task.get('owner', 'Unknown')}] {task.get('task', '')}"
                for task in data["tasks"]
            ])
            properties["Tasks"] = {
                "rich_text": [
                    {
                        "text": {
                            "content": tasks_text[:2000]
                        }
                    }
                ]
            }
        
        # Confidence (number)
        if "confidence" in data:
            properties["Confidence"] = {
                "number": float(data["confidence"])
            }
        
        # Session ID (rich_text) - 추가 필드
        if "session_id" in data:
            properties["Session ID"] = {
                "rich_text": [
                    {
                        "text": {
                            "content": str(data["session_id"])
                        }
                    }
                ]
            }
        
        # Created At (date) - 자동으로 현재 시간
        properties["Created At"] = {
            "date": {
                "start": datetime.now().isoformat()
            }
        }
        
        return properties
    
    def test_connection(self) -> bool:
        """
        Notion 연결 테스트
        """
        try:
            self.client.databases.retrieve(database_id=self.database_id)
            return True
        except Exception as e:
            print(f"Notion 연결 실패: {e}")
            return False
