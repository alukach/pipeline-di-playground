from enum import Enum
from importlib import import_module


class CloudProvider(str, Enum):
    local = "local"
    aws = "aws"


def bootstrap(env: CloudProvider):
    """
    Import local provider classes from file matching cloud provider.
    """
    import_module(f".{env}", package=__name__)
