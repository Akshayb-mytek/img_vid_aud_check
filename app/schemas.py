# app/schemas.py

from pydantic import BaseModel, HttpUrl, Field
from typing import Literal

class AnalyzeRequest(BaseModel):
    url: HttpUrl
    frames_per_second: int = 10
    contentType: Literal["image", "video"] = Field(
        default="video",
        description="Type of content"
    )