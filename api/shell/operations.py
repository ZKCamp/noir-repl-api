import os
import subprocess


class ShellOperations:
    def __init__(self):
        pass

    @staticmethod
    def _run_command(command, cwd):
        command = command.split()
        process = subprocess.run(
            command, capture_output=True, cwd=cwd, check=False
        )

        return process.returncode, process.stdout, process.stderr

    def initialise_noir_project(self, project_name, directory):
        command = f"nargo new {project_name}"
        ret_code, output, _ = self._run_command(
            command, cwd=directory
        )

        assert (ret_code == 0)

    def compile_code(self, project_directory):
        command = f"nargo check"
        ret_code, output, error = self._run_command(
            command, cwd=project_directory
        )
        return ret_code, error

    def get_file_contents(self, file_path):
        command = f"cat {file_path}"

        ret_code, output, _ = self._run_command(
            command, cwd=os.getcwd()
        )

        assert (ret_code == 0)
        return output

    def prove(self, directory):
        command = f"nargo prove p"

        ret_code, output, error = self._run_command(
            command, cwd=directory
        )
        return ret_code, error

    def verify(self, directory):
        command = f"nargo verify p"

        ret_code, output, error = self._run_command(
            command, cwd=directory
        )

        return ret_code, error
