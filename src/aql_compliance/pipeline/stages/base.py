from abc import ABC
from abc import abstractmethod

from ..context import PipelineContext


class PipelineStage(ABC):

    @abstractmethod
    def run(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Mutate the pipeline context.
        """
        raise NotImplementedError