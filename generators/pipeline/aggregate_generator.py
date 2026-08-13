from .base_generator import CapabilityGenerator
from ...models import QueryNode

class AggregateGenerator(CapabilityGenerator):

    def __init__(
        self,
        builder: QueryBuilder,
        aggregate_registry: AggregateRegistry,
    ):
        self.builder = builder
        self.aggregate_registry = aggregate_registry

    def generate(
        self,
        manifest,
    ) -> QueryNode:

        root = QueryNode(
            name="aggregates",
        )

        #
        # Simple aggregate functions
        #

        for aggregate in self.aggregate_registry:

            query = self.builder.aggregate(
                manifest,
                aggregate,
            )

            root.add_child(
                QueryNode(
                    name=aggregate.name,
                    query=query,
                )
            )

        #
        # GROUP BY subtree
        #

        root.add_child(
            self._generate_group_by(
                manifest,
            )
        )

        return root

    def _generate_group_by(
            self,
            manifest,
        ) -> QueryNode:

        group = QueryNode(
            name="group_by",
            query=self.builder.group_by(
                manifest,
            ),
        )

        #
        # HAVING
        #

        group.add_child(
            QueryNode(
                name="having",
                query=self.builder.having(
                    manifest,
                ),
            )
        )

        return group