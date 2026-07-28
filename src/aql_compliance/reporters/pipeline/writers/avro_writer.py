
from ....module_loader import load
from pathlib import Path
from .base.dataframe_writer  import DataFrameWriter

from ....module_loader import load
from ....models import OutputFormat
from ..report_models import ReporterRole
from ..report_registry import reporter

@reporter(
    formats=[
        OutputFormat.AVRO,
    ],
    role=ReporterRole.WRITER,
)
class AvroWriter(
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

        records = (
            dataframe
            .to_dict(
                orient="records"
            )
        )

        schema = (
            fastavro
            .parse_schema(
                self._schema(
                    dataframe,
                    table_name,
                )
            )
        )

        with open(
            output_dir
            / f"{table_name}.avro",
            "wb",
        ) as fp:
            load("fastavro")
            import fastavro
            fastavro.writer(
                fp,
                schema,
                records,
            )

    def _schema(
        self,
        dataframe,
        table_name,
    ):

        fields = []

        for column in dataframe.columns:
            fields.append(
                {
                    "name": column,
                    "type": self._avro_type(
                        dataframe[column].dtype
                    ),
                }
            )

        return {
            "type": "record",
            "name": table_name,
            "fields": fields,
        }

    def _avro_type(self, dtype):
        load("pandas")
        import pandas as pd
        if pd.api.types.is_integer_dtype(dtype):
            return ["null", "long"]

        if pd.api.types.is_float_dtype(dtype):
            return ["null", "double"]

        if pd.api.types.is_bool_dtype(dtype):
            return ["null", "boolean"]

        return ["null", "string"]