# Pipeline + Dependency Injection Playground

This is an experiment to understand if we can write data pipelines in a way that you declare the supporting services that each step required, similar to how [FastAPI's Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) function. The manner in which each dependencies would be resolved would depend on its runtime environment, thus supporting pipelines that could run locally or in a cloud-based environment.

Additionally, each pipeline step should be able to inform cloud providers of its permission requirements when deployed.

## Design

### Interfaces

Interfaces serve as the basis for dependencies used by pipeline steps. For example, a step may require a secret loaded at runtime. Locally, this could be from a `.env` file while in a cloud environment this could be from a services, such as AWS Secrets Manager. This library handles both situations by allowing a handler to specify the interface that it depends on (eg a `Secret`) and at runtime the library will determine where this value should be loaded from and provide it via dependency injection.

### Reading

- Dependency Injection: https://www.netguru.com/blog/dependency-injection-with-python-make-it-easy
- Protocols: https://peps.python.org/pep-0544/
