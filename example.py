from playground import interfaces, pipeline, providers


# TODO: How to register configuration of dependencies? e.g. specify the queue name
def step_1(queue: interfaces.IQueue):
    print(queue)
    ...


p = pipeline.Pipeline(steps=[step_1])
p.run(providers.CloudProvider.aws)
