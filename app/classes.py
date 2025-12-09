from enum import Enum
from typing import TypedDict

from pydantic import BaseModel, Field

class NextState(str, Enum):
    ANSWER = 'answer'
    RAG = 'rag'
    UPLOADER = 'uploader'



class RouterOutput(BaseModel):
    next_state: NextState = Field(description='Название следующего состояния графа')
    reasoning: str = Field(description='Объяснение, почему выбрал именно его')