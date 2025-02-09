from app.models.base import BaseRequest, BaseResponse


########################################################
# Requests
########################################################
class ChatRequest(BaseRequest):
    query: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "안녕",
                }
            ]
        }
    }


########################################################
# Responses
########################################################
class ChatResponse(BaseResponse):
    data: dict

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "data": {"message": "무엇을 도와드릴까요?"},
                },
                {
                    "success": False,
                    "data": {"message": "에러가 발생했습니다.", "error": "..."},
                }

            ]
        }
    }
