EXECUTE_PLAN_REGISTRY = {}

def register_execution_plan(name):
    def decorator(cls):
        EXECUTE_PLAN_REGISTRY[name] = cls
        return cls
    return decorator