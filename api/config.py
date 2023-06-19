import os
from envyaml import EnvYAML


class Config:
    def __init__(self):
        self.current_path = os.path.dirname(os.path.realpath(__file__))

        self.examples_config = os.path.join(self.current_path, "configs/examples.yaml")

        self.sessions_dir = os.path.join(
            self.current_path,
            "../data/sessions"
        )
