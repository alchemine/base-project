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
                    "error_message": None,
                    "data": {"message": "무엇을 도와드릴까요?"},
                }
            ]
        }
    }
