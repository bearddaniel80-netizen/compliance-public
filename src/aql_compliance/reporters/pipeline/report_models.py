from dataclasses import dataclass, field
from typing import Any
from ...models import OutputFormat
from enum import StrEnum

class ReporterRole(StrEnum):
    RENDERER = "renderer"
    WRITER = "writer"

@dataclass
class FileArtifact:
    content: str | bytes
    binary: bool = False
    destination: str = "reports"
    output_file: str = ""

@dataclass
class ConsoleArtifact:
    renderable: object

@dataclass
class TableArtifact:
    tables: dict[
        str,
        list[dict]
    ]
    destination: str = "reports"
    output_file: str = ""

@dataclass
class SummaryModel:

    passed: int = 0

    failed: int = 0

    skipped: int = 0

    total: int = 0

    duration_ms: int = 0

    pass_rate: float = 0.0

    def to_dict(self):
        return {
            "total": self.total,
            "passed": self.passed,
            "skipped": self.skipped,
            "failed": self.failed,
            "duration_ms": self.duration_ms,
            "pass_rate": self.pass_rate
        }

class StatusType(StrEnum):
    PASS = "passed"
    SKIP = "skipped"
    FAIL = "failed"

@dataclass
class QueryModel:

    name: str

    query: str

    status: StatusType

    duration_ms: int

    error: str = ""

    def to_dict(self):
        return {
            "name": self.name,
            "query": self.query.text,
            "status": self.status,
            "error": self.error,
            "duration_ms": self.duration_ms
        }

@dataclass
class FailureModel:

    manifest: str

    query: str

    error: str
    
    def to_dict(self):
        return {
            "name": self.manifest,
            "query": self.query.text,
            "error": self.error
        }

@dataclass
class PerformanceModel:

    manifest: str

    query: str

    duration_ms: int

    def to_dict(self):
        return {
            "name": self.manifest,
            "query": self.query.text,
            "duration_ms": self.duration_ms
        }


@dataclass
class ReportData:

    summary: SummaryModel = None

    queries: list[QueryModel] = field(
        default_factory=list
    )

    failures: list[FailureModel] = field(
        default_factory=list
    )

    performance: list[
        PerformanceModel
    ] = field(
        default_factory=list
    )


@dataclass
class ReportContext:

    execution_context: Any

    content: Any = None # called from render stage

    report_data: ReportData | None = None

    artifact: Any = None

    output_format: OutputFormat = OutputFormat.RICH
