from pydantic import BaseModel, Field
from typing import Literal

class QuestRequest(BaseModel):
    duration_minutes: int = Field(default=20, ge=5, le=180)
    difficulty: Literal["easy", "medium", "challenging"] = "easy"
    setting: Literal["park", "garden", "neighborhood", "trail", "anywhere"] = "park"
    interests: str = Field(default="plants, birds, and small details", max_length=240)

class AskRequest(BaseModel):
    question: str = Field(min_length=2, max_length=1200)
    observation: str = Field(default="", max_length=1200)
