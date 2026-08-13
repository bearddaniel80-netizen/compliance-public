from .base_generator import CapabilityGenerator
from ...models import QueryNode

class OrderGenerator(CapabilityGenerator):

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
            name="order_by",
        )

        #
        # ORDER BY ASC
        #

        asc = QueryNode(
            name="ascending",
            query=self.builder.order_by(
                manifest,
                direction="ASC",
            ),
        )

        root.add_child(asc)

        #
        # ORDER BY DESC
        #

        desc = QueryNode(
            name="descending",
            query=self.builder.order_by(
                manifest,
                direction="DESC",
            ),
        )

        asc.add_child(desc)

        return root