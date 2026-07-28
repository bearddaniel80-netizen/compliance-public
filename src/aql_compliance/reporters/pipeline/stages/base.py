from abc import ABC
from abc import abstractmethod

class PipelineStage(ABC):

    @abstractmethod
    def run(
        self,
        context,
    ) -> None:
        """
        Mutate the pipeline context.
        """
        raise NotImplementedError