"""
Thinking Box MCP 서버

Anthropic MCP 표준을 따르는 실제 MCP 서버
Claude Desktop이나 다른 MCP 클라이언트에서 사용 가능
"""
import os
import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from notion_storage import NotionStorage


# MCP 서버 인스턴스
app = Server("thinking-box-mcp")

# Notion 클라이언트 (전역)
notion_client = None


def initialize_notion():
    """Notion 클라이언트 초기화"""
    global notion_client
    if notion_client is None:
        notion_client = NotionStorage()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    사용 가능한 도구 목록 반환
    """
    return [
        Tool(
            name="save_thinking_result",
            description="""
            Thinking Box 에이전트의 사고 결과를 Notion Database에 저장합니다.
            
            입력 형식:
            {
                "session_id": "세션 ID",
                "idea_stage": "발산 또는 수렴",
                "title": "아이디어 제목",
                "summary": "요약 내용",
                "key_points": ["핵심 포인트 1", "핵심 포인트 2"],
                "tasks": [
                    {"owner": "담당자", "task": "작업 내용"}
                ],
                "confidence": 0.87
            }
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "세션 고유 ID"
                    },
                    "idea_stage": {
                        "type": "string",
                        "enum": ["발산", "수렴"],
                        "description": "아이디어 단계"
                    },
                    "title": {
                        "type": "string",
                        "description": "아이디어 제목"
                    },
                    "summary": {
                        "type": "string",
                        "description": "요약 내용"
                    },
                    "key_points": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "핵심 포인트 리스트"
                    },
                    "tasks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "owner": {"type": "string"},
                                "task": {"type": "string"}
                            }
                        },
                        "description": "작업 목록"
                    },
                    "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                        "description": "신뢰도 (0~1)"
                    }
                },
                "required": ["title", "summary"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    도구 실행
    """
    if name != "save_thinking_result":
        raise ValueError(f"알 수 없는 도구: {name}")
    
    try:
        # Notion 클라이언트 초기화
        initialize_notion()
        
        # Notion에 저장
        result = notion_client.save_thinking_result(arguments)
        
        # 성공 메시지 반환
        return [
            TextContent(
                type="text",
                text=f"""✅ Notion에 저장 완료!

페이지 URL: {result['page_url']}
페이지 ID: {result['page_id']}
생성 시간: {result['created_time']}

저장된 내용:
- 제목: {arguments.get('title', 'N/A')}
- 단계: {arguments.get('idea_stage', 'N/A')}
- 요약: {arguments.get('summary', 'N/A')[:100]}...
"""
            )
        ]
    
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"❌ 저장 실패: {str(e)}"
            )
        ]


async def main():
    """
    MCP 서버 실행
    
    사용법:
        python mcp_server.py
    """
    # 환경 변수 로드
    from dotenv import load_dotenv
    load_dotenv()
    
    # stdio를 통해 서버 실행
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
