"""
Thinking Box HTTP API 서버

FastAPI 기반 REST API
외부 시스템에서 HTTP POST로 Notion에 데이터 저장
"""
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv

from notion_storage import NotionStorage


# 환경 변수 로드
load_dotenv()

# FastAPI 앱
app = FastAPI(
    title="Thinking Box API",
    description="Thinking Box 에이전트 결과를 Notion에 저장하는 REST API",
    version="1.0.0"
)

# Notion 클라이언트
notion_client = NotionStorage()


# 요청 모델
class Task(BaseModel):
    """작업 아이템"""
    owner: str = Field(..., description="담당자")
    task: str = Field(..., description="작업 내용")


class ThinkingResult(BaseModel):
    """Thinking Box 에이전트 출력"""
    session_id: str = Field(..., description="세션 고유 ID")
    idea_stage: str = Field(..., description="아이디어 단계: 발산 또는 수렴")
    title: str = Field(..., description="아이디어 제목")
    summary: str = Field(..., description="요약 내용")
    key_points: List[str] = Field(default_factory=list, description="핵심 포인트")
    tasks: List[Task] = Field(default_factory=list, description="작업 목록")
    confidence: float = Field(..., ge=0.0, le=1.0, description="신뢰도 (0~1)")
    
    @validator('idea_stage')
    def validate_stage(cls, v):
        if v not in ['발산', '수렴']:
            raise ValueError('idea_stage는 "발산" 또는 "수렴"이어야 합니다')
        return v


# 응답 모델
class IngestResponse(BaseModel):
    """저장 성공 응답"""
    success: bool
    page_id: str
    page_url: str
    created_time: str
    message: str


class ErrorResponse(BaseModel):
    """에러 응답"""
    success: bool = False
    error: str
    detail: Optional[str] = None


@app.get("/")
async def root():
    """헬스 체크"""
    return {
        "service": "Thinking Box MCP Server",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "ingest": "POST /ingest - Notion에 데이터 저장",
            "health": "GET /health - 서버 상태 확인"
        }
    }


@app.get("/health")
async def health_check():
    """
    서버 상태 및 Notion 연결 확인
    """
    notion_ok = notion_client.test_connection()
    
    return {
        "status": "healthy" if notion_ok else "degraded",
        "notion_connection": "ok" if notion_ok else "failed",
        "timestamp": datetime.now().isoformat()
    }


@app.post(
    "/ingest",
    response_model=IngestResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "데이터가 성공적으로 저장됨"},
        400: {"model": ErrorResponse, "description": "잘못된 입력 데이터"},
        500: {"model": ErrorResponse, "description": "서버 에러"}
    }
)
async def ingest_thinking_result(data: ThinkingResult):
    """
    Thinking Box 에이전트 결과를 Notion Database에 저장
    
    **요청 예시:**
    ```json
    {
        "session_id": "550e8400-e29b-41d4-a716-446655440000",
        "idea_stage": "발산",
        "title": "신규 기능 아이디어",
        "summary": "사용자 경험을 개선하는 새로운 기능 제안",
        "key_points": ["UX 개선", "성능 최적화"],
        "tasks": [
            {"owner": "FE", "task": "와이어프레임 작성"},
            {"owner": "BE", "task": "API 설계"}
        ],
        "confidence": 0.87
    }
    ```
    
    **응답 예시:**
    ```json
    {
        "success": true,
        "page_id": "abc123...",
        "page_url": "https://notion.so/...",
        "created_time": "2025-01-08T12:00:00.000Z",
        "message": "데이터가 성공적으로 저장되었습니다"
    }
    ```
    """
    try:
        # Notion에 저장
        result = notion_client.save_thinking_result(data.dict())
        
        return IngestResponse(
            success=True,
            page_id=result["page_id"],
            page_url=result["page_url"],
            created_time=result["created_time"],
            message="데이터가 성공적으로 저장되었습니다"
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"잘못된 데이터 형식: {str(e)}"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Notion 저장 실패: {str(e)}"
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP 예외 핸들러"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # 서버 실행
    uvicorn.run(
        "http_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
