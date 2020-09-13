from vertex.task import Task


class Router:
    def __init__(self, name, schema: dict):
        self.name = name
        self.schema = schema
        self.enabled = True

    def route_and_call(self, task: Task):
        func = self.route(task.path.to_arr()[1:])
        return func(task)

    def route(self, action_path: [str]):
        if len(action_path) == 0:
            raise Exception("Could not route, only functions can be routed. Ended at " + self.name + " prematurely")
        t = action_path[0]

        if t not in self.schema:
            raise KeyError("{} could not be routed, only {} are allowed".format(t, list(self.schema.keys())))

        step = self.schema[t]

        if callable(step):
            return step
        if type(step) == Router:
            if not step.enabled:
                raise Exception("cannot route to {}, it is disabled".format(step.name))
            return step.route(action_path[1:])

        raise TypeError("{} not allowed, only function and Router allowed in schema".format(str(type(step))))

    def get_child(self, path: str):
        return self.schema[path]

    def adopt(self, router: "Router") -> None:
        assert router.name not in self.schema
        self.schema[router.name] = router

    def disable(self, name):
        self.schema[name].enabled = False

    def enable(self, name):
        self.schema[name].enabled = True
