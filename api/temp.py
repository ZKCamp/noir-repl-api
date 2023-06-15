from api.config import Config
from session.manager import SessionManager
from shell.operations import ShellOperations


config = Config()
shell_ops = ShellOperations()
session_manager = SessionManager(config, shell_ops)


identifier = "6359b684-0b3a-11ee-8920-acde48001122"
print(
    session_manager.replace_inputs(identifier, {"x": 10, "y": 1283})
)
