from enum import Enum
from importlib import import_module

from kink import di


class CloudProvider(str, Enum):
    local = "local"
    aws = "aws"


def bootstrap(env: CloudProvider):
    """
    Import local provider classes from file matching cloud provider.
    """
    import_module(f".{env}", package=__name__)
    di[CloudProvider] = env
