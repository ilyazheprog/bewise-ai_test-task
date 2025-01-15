from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ApplicationCreate(BaseModel):
    user_name: str = Field(..., title="Имя пользователя", max_length=100)
    description: str = Field(..., title="Описание", max_length=255)

class ApplicationUpdate(BaseModel):
    user_name: str | None = Field(None, title="Имя пользователя", max_length=100)
    description: str | None = Field(None, title="Описание", max_length=255)

class ApplicationResponse(BaseModel):
    id: int
    user_name: str
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
