from pydantic import BaseModel


class BaseRequest(BaseModel):
    pass


class BaseResponse(BaseModel):
    success: bool
    error_message: str | None = None
