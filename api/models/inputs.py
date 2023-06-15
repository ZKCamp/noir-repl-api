from pydantic import BaseModel
from typing import Dict


class CodeInput(BaseModel):
    session_id: str
    code: str


class Input(BaseModel):
    session_id: str
    inputs: Dict
