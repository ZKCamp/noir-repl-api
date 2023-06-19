from fastapi import FastAPI
from api.config import Config
from session.manager import SessionManager
from shell.operations import ShellOperations

from models.inputs import CodeInput, ParamInput, RunInput, SessionCreationInput
from models.outputs import CodeOutput, RunOutput

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


@app.post("/session/create")
async def create_session(session_creation_input: SessionCreationInput):
    session_identifier, code, inputs = session_manager.create_session(
        session_creation_input.name,
        session_creation_input.session_type
    )

    return {
        "session_id": session_identifier,
        "code": code,
        "inputs": inputs
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

    return RunOutput(
        session_id=session_id,
        is_compiled=True if ret_code == 0 else False,
        output=output
    )


@app.post("/session/run")
async def run(run_input: RunInput):
    session_manager.replace_code(run_input.session_id, run_input.code)
    session_manager.replace_inputs(run_input.session_id, run_input.inputs)

    ret_code, output = session_manager.compile_code(run_input.session_id)

    if ret_code != 0:
        return RunOutput(
            session_id=run_input.session_id,
            is_compiled=True if ret_code == 0 else False,
            output=output
        )

    ret_code, output = session_manager.generate_proof(run_input.session_id)

    return RunOutput(
        session_id=run_input.session_id,
        is_compiled=True if ret_code == 0 else False,
        output=output
    )


@app.post("/session/inputs/change")
async def replace_inputs(inputs: ParamInput):
    input_params = inputs.inputs
    session_id = inputs.session_id

    session_manager.replace_inputs(session_id, input_params)
    return {
        "message": "Success"
    }


@app.post("/session/proof/{session_id}")
async def generate_proof(session_id: str):
    ret_code, output = session_manager.generate_proof(session_id)

    return RunOutput(
        session_id=session_id,
        is_compiled=True if ret_code == 0 else False,
        output=output
    )


@app.get("/examples")
async def get_examples():
    example_names = session_manager.get_example_names()
    return example_names


@app.get("/session/{session_id}")
async def get_session_info(session_id: str):
    code, inputs = session_manager.get_session_info(session_id)

    return {
        "code": code,
        "inputs": inputs
    }
