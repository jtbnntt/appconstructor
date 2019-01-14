class Service:
    def __init__(self, dependency, value, global_value):
        self.dependency = dependency
        self.value = value
        self.global_value = global_value

class OtherService:
    def __init__(self, value):
        self.value = value

class AnotherService:
    def __init__(self, value):
        self.value = value
