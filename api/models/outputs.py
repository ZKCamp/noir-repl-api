from pydantic import BaseModel


class CodeOutput(BaseModel):
    session_id: str
    code: str


class RunOutput(BaseModel):
    session_id: str
    output: str
    is_compiled: str
