from pydantic import BaseModel
from playground import services, providers
from playground.primitives import step, Pipeline


class Input(BaseModel):
    ...


class Output(Input):
    ...


@step(deps={"secret_1": lambda di: "foo", "secret_2": lambda di: "bar"})
def test_step(
    data_in: Input, queue: services.IQueue, secret_1: str, secret_2: str
) -> Input:
    print(f"Running with {queue=} {secret_1=} {secret_2=}")
    return data_in


if __name__ == "__main__":
    p = Pipeline[Input, Output](env=providers.CloudProvider.local, steps=[test_step])
    output = p.run(Input())
