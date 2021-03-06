from typing import cast
from pydantic import BaseModel
from playground.services import IQueue, ISecret
from playground.providers import CloudProvider
from playground.primitives import step, Pipeline, EnvVar


class Input(BaseModel):
    name: str
    age: int


class Output(Input):
    ...


@step(
    deps={
        "secret_1_arn": EnvVar("SECRET_1_ARN"),
        "secret_2_arn": EnvVar("SECRET_2_ARN"),
        "secret_1": lambda di: di[ISecret].get(di["secret_1_arn"]),
        "secret_2": lambda di: di[ISecret].get(di["secret_2_arn"]),
    },
    aws_lambda_properties={"memory": 3024, "timeout": 180},
)
def kitchen_sink(
    data_in: Input, queue: IQueue, secret_1: str, secret_2: str, env: CloudProvider
) -> Output:
    print("Dependency resolutions:")
    print(f" - {env=}")
    print(f" - {queue=}")
    print(f" - {secret_1=}")
    print(f" - {secret_2=}")
    return cast(Output, data_in)


@step
def make_knight(data_in: Input) -> Output:
    data_in.name = f"Sir {data_in.name}"
    return cast(Output, data_in)


@step
def make_old(data_in: Input) -> Output:
    data_in.age += 50
    return cast(Output, data_in)


pipeline = Pipeline[Input, Output](
    name="Example Pipeline", steps=[kitchen_sink, make_knight, make_old]
)


if __name__ == "__main__":
    output = pipeline.run(Input(name="Ringo Star", age=24))
    print(f"{output=}")
