import os
import uuid

from glob import glob
import toml

from api.utils import clean_output


class SessionManager:
    def __init__(self, config, shell_ops):
        self.sessions_dir = config.sessions_dir
        self.shell_ops = shell_ops

    def create_session(self, project_name):
        try:
            session_identifier = uuid.uuid1()
            session_dir_name = f"{session_identifier}__{project_name}"
            session_directory = os.path.join(self.sessions_dir, session_dir_name)

            os.mkdir(session_directory)

            self.shell_ops.initialise_noir_project(project_name, session_directory)

            return session_identifier

        except Exception:
            raise Exception("Failed to create session")

    def get_session(self, identifier):
        session_dir = glob(f"{self.sessions_dir}/{identifier}__*")[0]
        project_name = session_dir.split("/")[-1].split("__")[1]
        project_dir = os.path.join(session_dir, project_name)

        return project_name, session_dir, project_dir

    def get_session_code(self, identifier):
        project_name, session_dir, project_dir = self.get_session(identifier)

        return self.shell_ops.get_file_contents(os.path.join(project_dir, "src", "main.nr")).decode("utf-8")

    def replace_code(self, identifier, code):
        project_name, session_dir, project_dir = self.get_session(identifier)

        with open(os.path.join(project_dir, "src", "main.nr"), "w") as file:
            file.truncate(0)
            file.write(code)

    def compile_code(self, identifier):
        project_name, session_dir, project_dir = self.get_session(identifier)

        ret_code, output = self.shell_ops.compile_code(project_dir)
        output = clean_output(output.decode("utf-8"))

        return ret_code, output

    def replace_inputs(self, identifier, inputs):
        project_name, session_dir, project_dir = self.get_session(identifier)

        toml_repr = toml.dumps(inputs)

        with open(os.path.join(project_dir, "Prover.toml"), "w") as fl:
            fl.truncate(0)
            fl.write(toml_repr)
