from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from enum import StrEnum


class QueryType(StrEnum):
    DESCRIBE = "DESCRIBE"
    SELECT = "SELECT"
    SHOW = "SHOW"

class OutputFormat(StrEnum):
    ARROW = "arrow"
    AVRO = "avro"
    CSV = "csv"
    DUCKDB = "duckdb"
    GITHUB = "github"
    HTML = "html"
    JSON = "json"
    JUNIT = "xml"
    MARKDOWN = "md"
    MYSQL = "mysql"
    PARQUET = "parquet"
    PDF = "pdf"
    POSTGRES = "postgres"
    RICH = "rich"
    SQLITE = "sqlite"

@dataclass
class PipelineConfig:

    fixture_dir: Path

    output_format: OutputFormat

    cache: bool = False

    retry: int = 0

    profile: bool = False

    parallel: int = 1

    fail_fast: bool = False

    fail_fast_query: bool = False

@dataclass
class TestResult:
    name: str
    query: str
    output: str
    passed: bool
    skipped: bool = False
    error: str | None = None
    duration_ms: int = 0

    def __repr__(self):
        return (
            "TestResult( " +
            f"name={self.name} " +
            f"query={self.query} " +
            f"output={self.output} " +
            f"skipped={self.skipped} " +
            f"error={self.error} " +
            f"duration_ms={self.duration_ms} " +
            ")"
        )

    def to_dict(self):
        return (
            {
                "name": self.name,
                "query": self.query.text,
                "skipped": self.skipped,
                "error": self.error,
                "duration_ms": self.duration_ms,
            }
        )
# -------- Executor -----

@dataclass
class ExecutionResult:

    command: str

    stdout: str

    stderr: str

    returncode: int

    duration_ms: int

    @property
    def success(
        self,
    ) -> bool:

        return self.returncode == 0

# ------- Generator / Validator ------

@dataclass
class Query:

    query_type: QueryType

    text: str

    expected_to_fail: bool = False

    def to_dict(self):
        return (
            {
                "query_type": self.query_type.value,
                "text": self.text,
                "expected_to_fail": self.expected_to_fail
            }
        )
@dataclass
class QueryNode:

    name: str

    query: Query

    children: list["QueryNode"] = field(
        default_factory=list
    )

    def add_child(
        self,
        node: "QueryNode",
    ) -> None:

        self.children.append(
            node
        )

    @property
    def is_leaf(
        self,
    ) -> bool:

        return not self.children
@dataclass
class TestNode:

    name: str

    query_type: QueryType

    query: str

    children: list["TestNode"] = field(
        default_factory=list
    )

# --------- Runner --------
@dataclass
class Args:
    manifest: str
    manifest_dir: Path | None = None
    fixture_dir: Path | None = None

@dataclass
class RunContext:
    fixture_data: str
    fail_fast_query: bool = False
# --------- Suite ----------

@dataclass
class Suite:
    name: str
    manifests: str | None = None
    # children: list["SuiteNode"] = field(default_factory=list)

# ---------- Manifest -------

class SourceType(StrEnum):
    FILE = "file"
    STDIN_API = "stdin_api"
    STDIN_FILE = "stdin_file"
    STDIN_RAW = "stdin_raw"
    VIRTUAL = "virtual"

class FilterOperator(StrEnum):
    EQ = "="
    NE = "!="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    IN = "IN"
    # LIKE = "LIKE"

@dataclass
class Filter:
    field: str
    operator: FilterOperator
    value: Any

@dataclass
class InputConfig:
    type: str
    fixture: str
    source: SourceType

@dataclass
class AssertionConfig:
    min_rows: int = 1
    required_fields: list[str] = field(default_factory=list)

@dataclass
class Manifest:
    name: str
    input: InputConfig
    fields: list[str]
    filters: list[Filter] = field(
        default_factory=list
    )
    assertions: AssertionConfig = field(
        default_factory=AssertionConfig
    )
    tags: list[str] = field(
        default_factory=list
    )