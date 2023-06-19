import os
import uuid

import json
import toml
import yaml

from glob import glob
from pathlib import Path

from api.utils import clean_output


class SessionManager:
    def __init__(self, config, shell_ops):
        self.examples_config = yaml.safe_load(Path(config.examples_config).read_text())
        self.sessions_dir = config.sessions_dir
        self.shell_ops = shell_ops

    def create_session(self, project_name, example_name):
        try:
            session_identifier = uuid.uuid1()
            session_dir_name = f"{session_identifier}__{project_name}"
            session_directory = os.path.join(self.sessions_dir, session_dir_name)

            os.mkdir(session_directory)

            self.shell_ops.initialise_noir_project(project_name, session_directory)

            example = self.get_example(example_name)
            self.replace_code(session_identifier, example["code"])
            self.replace_inputs(session_identifier, json.loads(example["inputs"]))

            return session_identifier, example["code"], example["inputs"]

        except Exception as exp:
            raise Exception(exp)

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

    def get_session_inputs(self, project_dir):
        inputs = toml.load(open(os.path.join(project_dir, "Prover.toml")))
        json_inputs = json.dumps(inputs)
        return json_inputs

    def generate_proof(self, identifier):
        project_name, session_dir, project_dir = self.get_session(identifier)

        ret_code, output = self.shell_ops.prove(project_dir)
        output = clean_output(output.decode("utf-8"))
        return ret_code, output

    def get_example_names(self):
        return [example["name"] for _, example in self.examples_config.items()]

    def get_example(self, example_name):
        for example in self.examples_config.values():
            if example["name"] == example_name:
                return example

    def get_session_info(self, identifier):
        project_name, session_dir, project_dir = self.get_session(identifier)

        code = self.get_session_code(identifier)
        inputs = self.get_session_inputs(project_dir)

        return code, inputs

    def test_execution(self):
        session_identifier = uuid.uuid1()
        session_dir_name = f"{session_identifier}__hello"
        session_directory = os.path.join(self.sessions_dir, session_dir_name)

        os.mkdir(session_directory)

        output, ret_code = self.shell_ops.temp_initialise_noir_project("temp", session_directory)
        return output, ret_code

