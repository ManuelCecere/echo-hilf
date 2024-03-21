from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str = "testing"
    conversation_id: str = "testing"
    question: str
