import os


class Config:
    def __init__(self):
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.sessions_dir = os.path.join(
            self.current_path,
            "../data/sessions"
        )
