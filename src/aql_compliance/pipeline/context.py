from dataclasses import dataclass
from dataclasses import field

from ..models import (
    Manifest,
    TestNode,
    TestResult,
)

from .execution_plan.base import ExecutionPlan

@dataclass
class PipelineContext:

    #
    # Inputs
    #
    manifest_name: str

    #
    # Loaded by stages
    #
    manifest: Manifest | None = None

    fixture_data: str | None = None

    tree: TestNode | None = None

    execution_plan: ExecutionPlan | None = None

    #
    # Execution output
    #
    results: list[TestResult] = field(
        default_factory=list
    )

    #
    # Runtime flags
    #
    fail_fast: bool = False

    fail_fast_query: bool = False

    profile: bool = False

    #
    # Metrics
    #
    duration_ms: int = 0

    #
    # Extensibility
    #
    metadata: dict = field(
        default_factory=dict
    )

    def __repr__(self):
        return (
            "PipelineContext( " +
            f"manifest_name={self.manifest_name} " +
            f"duration_ms={self.duration_ms} " +
            ")"
        )