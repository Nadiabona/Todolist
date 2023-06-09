from typing import Optional

from pydantic import BaseModel

class Chat(BaseModel):
    id: int


class Message(BaseModel):
    chat: Chat
    text: Optional[str] = None


class UpdateObj(BaseModel):
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: list[UpdateObj]


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message