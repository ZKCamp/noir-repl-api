from api.config import Config
from session.manager import SessionManager
from shell.operations import ShellOperations

from models.inputs import SessionCreationInput


config = Config()
shell_ops = ShellOperations()
session_manager = SessionManager(config, shell_ops)

session_input = SessionCreationInput(session_type="Hello World", name="temp")
identifier = "1118e084-0b5d-11ee-bb59-acde48001122"
print(
    session_manager.get_session_info(identifier)
)
