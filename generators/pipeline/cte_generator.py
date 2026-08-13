from .base_generator import CapabilityGenerator
from ...models import QueryNode

class CteGenerator(CapabilityGenerator):

    def __init__(
        self,
        builder: QueryBuilder,
    ):
        self.builder = builder

    def generate(
        self,
        manifest,
    ) -> QueryNode:

        root = QueryNode(
            name="cte",
        )

        #
        # Basic CTE
        #

        simple = QueryNode(
            name="simple",
            query=self.builder.simple_cte(
                manifest,
            ),
        )

        root.add_child(simple)

        #
        # Multiple CTEs
        #

        multiple = QueryNode(
            name="multiple",
            query=self.builder.multiple_ctes(
                manifest,
            ),
        )

        simple.add_child(multiple)

        #
        # Chained CTEs
        #

        chained = QueryNode(
            name="chained",
            query=self.builder.chained_ctes(
                manifest,
            ),
        )

        multiple.add_child(chained)

        #
        # Aggregate CTE
        #

        aggregate = QueryNode(
            name="aggregate",
            query=self.builder.aggregate_cte(
                manifest,
            ),
        )

        chained.add_child(aggregate)

        #
        # Recursive CTE (optional)
        #

        recursive = QueryNode(
            name="recursive",
            query=self.builder.recursive_cte(
                manifest,
            ),
        )

        aggregate.add_child(recursive)

        return root