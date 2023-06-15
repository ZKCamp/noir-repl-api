from fastapi import FastAPI
from api.config import Config
from session.manager import SessionManager
from shell.operations import ShellOperations

from models.inputs import CodeInput, Input
from models.outputs import CodeOutput, CompilationOutput

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = Config()
shell_ops = ShellOperations()
session_manager = SessionManager(config, shell_ops)


@app.get("/")
async def root():
    return {"message": f"Welcome to NoirRepl"}


@app.post("/session/create/{name}")
async def create_session(name: str):
    session_manager.create_session(name)

    return {
        "message": "Success"
    }


@app.get("/session/code/{session_id}")
async def get_session_code(session_id: str):
    return CodeOutput(
        code=session_manager.get_session_code(session_id),
        session_id=session_id
    )


@app.post("/session/code/change")
async def replace_code(code_input: CodeInput):
    session_code = code_input.code
    session_id = code_input.session_id

    session_manager.replace_code(session_id, session_code)

    return {
        "message": "Success"
    }


@app.get("/session/code/compile/{session_id}")
async def compile_code(session_id: str):
    ret_code, output = session_manager.compile_code(session_id)

    return CompilationOutput(
        session_id=session_id,
        is_compiled=True if ret_code == 0 else False,
        output=output
    )


@app.post("/session/inputs/change")
async def replace_inputs(inputs: Input):
    input_params = inputs.inputs
    session_id = inputs.session_id

    session_manager.replace_inputs(session_id, input_params)
    return {
        "message": "Success"
    }
