#Schemas(DTOs)

from pydantic import BaseModel, Field

# Browser-generated UUIDs match this. Validating stops junk or oversized ids or unsual ids.
SESSION_ID_PATTERN = r"^[A-Za-z0-9-]{8,64}$"

class ChatRequest(BaseModel):
    session_id: str = Field(pattern=SESSION_ID_PATTERN)
    message: str = Field(min_length= 1, max_length= 500)


class ChatResponse(BaseModel):
    reply: str
    total_tokens: int