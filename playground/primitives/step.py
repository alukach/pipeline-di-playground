from dataclasses import field, dataclass
from typing import Any, Callable, Generic, Mapping, Type, TypeVar, Union

from kink import inject, di
from pydantic import BaseModel

from ..primitives.env_var import EnvVar
from ..providers import CloudProvider, bootstrap


Input = TypeVar("Input", contravariant=True, bound=BaseModel)
Output = TypeVar("Output", covariant=True, bound=BaseModel)


@dataclass
class Step(Generic[Input, Output]):
    handler: Callable[[Input], Output]
    deps: Mapping[Union[str, Type], Any] = field(default_factory=dict)
    aws_lambda_properties: Mapping[str, Any] = field(default_factory=dict)

    def __call__(self, input: Input) -> Output:
        """
        Inject dependencies & execute step.
        """
        # TODO: How can load Pydantic model from JSON-dict input?
        for key, value in self.deps.items():

            # Resolve env vars
            if isinstance(value, EnvVar):
                value = value.value

            di[key] = value
        prepped_handler = inject(self.handler)
        return prepped_handler(input)
        # TODO: How can we export back to JSON-dict?

    def lambda_handler(self, event, context):
        """
        Handler for AWS Lambdas.
        """
        # When running in lambda, we don't instantiate a Pipeline class (where
        # bootstrapping occurs), so we must bootstrap our DI here
        bootstrap(CloudProvider.aws)
        return self(event)


def step(func=None, *args, **kwargs):
    """
    Decorator to create Step object from func
    """
    # decorator not called as function, eg: @step
    if func:
        return Step(handler=func, *args, **kwargs)

    # decorator called as function, eg: @step()
    def wrapper(_func):
        return Step(handler=_func, *args, **kwargs)

    return wrapper
