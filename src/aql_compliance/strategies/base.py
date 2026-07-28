from abc import ABC
from abc import abstractmethod

class RunnerStrategy(
    ABC
):
    
    @abstractmethod
    def build_contexts(
        self,
        config,
    ):
        pass