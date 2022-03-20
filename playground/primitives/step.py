from dataclasses import field, dataclass
from typing import Any, Callable, Generic, Mapping, Protocol, Type, TypeVar, Union

from kink import inject, di
from pydantic import BaseModel

from playground.providers import CloudProvider, bootstrap


Input = TypeVar("Input", contravariant=True, bound=BaseModel)
Output = TypeVar("Output", covariant=True, bound=BaseModel)


@dataclass
class Step(Generic[Input, Output]):
    handler: Callable[[Input], Output]
    deps: Mapping[Union[str, Type], Any] = field(default_factory=dict)

    def __call__(self, input: Input) -> Output:
        """
        Inject dependencies & execute step.
        """
        for key, value in self.deps.items():
            di[key] = value
        prepped_handler = inject(self.handler)
        return prepped_handler(input)

    def lambda_handler(self, event, context):
        """
        Handler for AWS Lambdas.
        """
        # When running in lambda, we don't instantiate a Pipeline class (where
        # bootstrapping occurs), so we must bootstrap our DI here
        bootstrap(CloudProvider.aws)
        return self(event)


def step(*args, **kwargs) -> Callable[..., Step]:
    """
    Decorator to create Step object from func
    """

    def wrapper(func):
        return Step(handler=func, *args, **kwargs)

    return wrapper
