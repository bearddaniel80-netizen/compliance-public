from .base.dataframe_writer import DataFrameWriter
from pathlib import Path

from ....models import OutputFormat
from ..report_models import ReporterRole
from ..report_registry import reporter

@reporter(
    formats=[
        OutputFormat.PARQUET,
    ],
    role=ReporterRole.WRITER,
)
class ParquetWriter(
    DataFrameWriter
):

    def write_dataframe(
        self,
        table_name,
        dataframe,
    ) -> None:

        output_dir = Path.cwd() / self.destination

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        dataframe.to_parquet(
            output_dir
            / f"{table_name}.parquet",
            index=False,
        )