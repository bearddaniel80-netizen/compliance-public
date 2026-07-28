from abc import (
    ABC,
    abstractmethod,
)

from .....module_loader import load


class TableWriter(
    ABC
):

    def write(
        self,
        artifact,
    ) -> None:

        self.destination = artifact.output_file

        connection = (
            self.connect()
        )
        load("pandas")
        import pandas as pd

        try:

            for (
                table_name,
                rows,
            ) in artifact.tables.items():

                if not rows:
                    continue

                if isinstance(rows, dict):
                    rows = [rows]

                if hasattr(rows, "to_dict") and not isinstance(rows, list):
                    rows = [rows.to_dict()]

                dataframe = (
                    pd.DataFrame(
                        rows
                    )
                )

                self.write_table(
                    connection=connection,
                    table_name=table_name,
                    dataframe=dataframe,
                )

        finally:

            connection.close()

    @abstractmethod
    def connect(
        self,
    ):
        pass

    def write_table(
        self,
        connection,
        table_name,
        dataframe,
    ) -> None:

        dataframe.to_sql(
            name=table_name,
            con=connection,
            if_exists="replace",
            index=False,
        )