from .pipeline.aggregate_generator import AggregateGenerator
from .pipeline.filter_generator import FilterGenerator
from .pipeline.logic_generator import LogicalGenerator
from .pipeline.orderby_generator import OrderGenerator
from .pipeline.projection_generator import ProjectionGenerator
from ..models import QueryNode

class TreeGenerator:

    def generate(self, manifest):

        root = QueryNode(
            "show",
            self.builder.show(manifest)
        )

        describe = QueryNode(
            "describe",
            self.builder.describe(manifest)
        )

        root.add_child(describe)

        select = QueryNode(
            "select",
            self.builder.select_star(manifest)
        )

        describe.add_child(select)

        #
        # Ask each capability generator
        #

        ProjectionGenerator().generate(
            manifest,
            select,
        )

        FilterGenerator().generate(
            manifest,
            select,
        )

        AggregateGenerator().generate(
            manifest,
            select,
        )

        OrderGenerator().generate(
            manifest,
            select,
        )

        CteGenerator().generate(
            manifest,
            select,
        )

        return root