from ..models import (
    Filter,
    FilterOperator,
    Query,
    QueryNode,
    QueryType,
)


class TreeGenerator:

    def generate(
        self,
        manifest,
    ) -> QueryNode:

        show_node = QueryNode(
            name="show",
            query=Query(
                query_type=QueryType.SHOW,
                text="SHOW source",
            ),
        )

        describe_node = QueryNode(
            name="describe",
            query=Query(
                query_type=QueryType.DESCRIBE,
                text="DESCRIBE source",
            ),
        )

        select_star_node = QueryNode(
            name="select_star",
            query=Query(
                query_type=QueryType.SELECT,
                text="SELECT * FROM source",
            ),
        )

        select_fields_node = QueryNode(
            name="select_fields",
            query=Query(
                query_type=QueryType.SELECT,
                text=(
                    f"SELECT "
                    f"{self._render_fields(manifest.fields)} "
                    f"FROM source"
                ),
            ),
        )

        show_node.add_child(
            describe_node
        )

        describe_node.add_child(
            select_star_node
        )

        select_star_node.add_child(
            select_fields_node
        )

        #
        # Add one child query per filter
        #

        for filter_ in manifest.filters:

            select_fields_node.add_child(
                QueryNode(
                    name=(
                        f"{filter_["field"]}_"
                        f"{filter_["operator"]}"
                    ),
                    query=Query(
                        query_type=QueryType.SELECT,
                        text=self._build_filter_query(
                            manifest,
                            filter_,
                        ),
                    ),
                )
            )

        return show_node

    def _build_filter_query(
        self,
        manifest,
        filter_: Filter,
    ) -> str:

        return (
            f"SELECT "
            f"{self._render_fields(manifest.fields)} "
            f"FROM source "
            f"WHERE "
            f"{self._render_filter(filter_)}"
        )

    def _render_filter(
        self,
        filter_: Filter,
    ) -> str:

        if (
            filter_["operator"]
            == FilterOperator.IN
        ):

            values = ", ".join(
                self._render_value(value)
                for value
                in filter_["value"]
            )

            return (
                f"{filter_["field"]} "
                f"IN [{values}]"
            )

        return (
            f"{filter_["field"]} "
            f"{filter_["operator"]} "
            f"{self._render_value(filter_["value"])}"
        )

    def _render_fields(
        self,
        fields: list[str],
    ) -> str:

        return ", ".join(
            fields
        )

    def _render_value(
        self,
        value,
    ) -> str:

        if isinstance(
            value,
            bool,
        ):
            return str(
                value
            ).lower()

        if value is None:
            return "null"

        if isinstance(
            value,
            (int, float),
        ):
            return str(value)

        return f"'{value}'"