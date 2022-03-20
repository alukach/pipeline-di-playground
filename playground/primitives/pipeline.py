from dataclasses import dataclass
from typing import (
    Callable,
    Generic,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    cast,
    runtime_checkable,
)

from kink import inject
from pydantic import BaseModel

from ..primitives.step import Step
from ..providers import CloudProvider, bootstrap

Input_co = TypeVar("Input_co", contravariant=True, bound=BaseModel)
Output = TypeVar("Output", covariant=True, bound=BaseModel)


@dataclass
class Pipeline(Generic[Input_co, Output]):
    env: CloudProvider
    steps: Sequence[Step]

    def __post_init__(self):
        bootstrap(self.env)

    def run(self, input: Input_co) -> Output:
        """
        Local execution of a pipeline
        """
        output = input
        for step in self.steps:
            output = step(output)
        return cast(Output, output)
