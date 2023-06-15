from api.config import Config
from session.manager import SessionManager
from shell.operations import ShellOperations


config = Config()
shell_ops = ShellOperations()
session_manager = SessionManager(config, shell_ops)


identifier = "1118e084-0b5d-11ee-bb59-acde48001122"
print(
    session_manager.compile_code(identifier)
)
