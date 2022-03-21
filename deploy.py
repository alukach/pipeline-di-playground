from playground.primitives import EnvVar

from example import pipeline


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


if __name__ == "__main__":
    """
    At time of deployment, we will inspect the pipeline and determine what needs to be created.
    """

    print(f"{color.BOLD}Deploying our pipeline:{color.END}")

    for step in pipeline.steps:
        print(f"\n  {color.BOLD}λ: {step.handler.__name__}{color.END}")

        print(
            f"    {color.ITALIC}FILENAME:{color.END} {step.handler.__code__.co_filename}"
        )
        print(
            f"    {color.ITALIC}ENTRYPOINT:{color.END} {step.handler.__name__}.lambda_handler"
        )

        print(f"    {color.ITALIC}ENV:{color.END}")
        env_vars = [v for v in step.deps.values() if isinstance(v, EnvVar)]
        for var in env_vars:
            print(f"      {var.name}={var.value}")
        if not env_vars:
            print("      (None)")

        print(f"    {color.ITALIC}CONFIG:{color.END} {step.aws_lambda_properties}")

        # TODO: Add permissions

    print(f"\n  {color.BOLD}SFN: {pipeline.name}{color.END}")
    print("    " + " -> ".join(s.handler.__name__ for s in pipeline.steps))
