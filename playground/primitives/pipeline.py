from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar, cast

from pydantic import BaseModel

from ..primitives.step import Step
from ..providers import CloudProvider, bootstrap

Input = TypeVar("Input", contravariant=True, bound=BaseModel)
Output = TypeVar("Output", covariant=True, bound=BaseModel)


@dataclass
class Pipeline(Generic[Input, Output]):
    name: str
    steps: Sequence[Step]

    def run(self, input: Input) -> Output:
        """
        Local execution of a pipeline
        """
        bootstrap(CloudProvider.local)

        output = input
        for step in self.steps:
            output = step(output)
        return cast(Output, output)
