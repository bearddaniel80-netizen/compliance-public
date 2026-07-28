from .base.dataframe_writer import DataFrameWriter
from pathlib import Path

from ....models import OutputFormat
from ..report_models import ReporterRole
from ..report_registry import reporter
from ....module_loader import load

@reporter(
    formats=[
        OutputFormat.ARROW,
    ],
    role=ReporterRole.WRITER,
)
class ArrowWriter(
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

        load("pyarrow")
        import pyarrow as pa
        import pyarrow.ipc as ipc
        table = (
            pa.Table
            .from_pandas(
                dataframe
            )
        )

        file_path = (
            output_dir
            / f"{table_name}.arrow"
        )

        with pa.OSFile(
            str(file_path),
            "wb",
        ) as sink:

            with ipc.new_file(
                sink,
                table.schema,
            ) as writer:

                writer.write(
                    table
                )