from typing import Callable, Sequence
from dataclasses import dataclass

from kink import inject

from .providers import CloudProvider, bootstrap


@dataclass
class Pipeline:
    steps: Sequence[Callable]

    def run(self, env: CloudProvider):
        bootstrap(env)
        for step in self.steps:
            func = inject(step)
            return func()
