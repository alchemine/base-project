from fastapi import APIRouter

from app.models.chat import ChatRequest, ChatResponse
from src.common.logger import log_error

router = APIRouter()


@router.post(
    "/completions",
    response_model=ChatResponse,
    description="Chat",
    tags=["chat"],
)
def completions(request: ChatRequest) -> ChatResponse:
    try:
        message = "무엇을 도와드릴까요?"
        result = ChatResponse(success=True, data={"message": message})
    except Exception as e:
        error_message = f"Failed to chat: {e}"
        log_error(error_message, exc_info=e)
        result = ChatResponse(
            success=False,
            data={
                "message": "죄송합니다. 문제가 발생했습니다.",
                "error": error_message,
            },
        )
    return result
