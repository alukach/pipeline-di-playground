from dataclasses import dataclass
import os


@dataclass
class EnvVar:
    """
    A dependency on an environment variable.
    """
    var_name: str

    def resolve(self):
        return os.environ[self.var_name]
