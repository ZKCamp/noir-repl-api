from pydantic import BaseModel
from typing import Dict


class CodeInput(BaseModel):
    session_id: str
    code: str


class ParamInput(BaseModel):
    session_id: str
    inputs: dict


class RunInput(BaseModel):
    session_id: str
    code: str
    inputs: dict


class SessionCreationInput(BaseModel):
    session_type: str
    name: str
