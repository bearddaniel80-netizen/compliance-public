from .base_generator import CapabilityGenerator
from ...models import QueryNode

class LogicalGenerator(CapabilityGenerator):

    def generate(
        self,
        manifest,
    ) -> QueryNode:

        root = QueryNode("logical")

        root.add_child(
            QueryNode(
                "NOT",
                self.builder.not_query(manifest),
            )
        )

        root.add_child(
            QueryNode(
                "AND",
                self.builder.and_query(manifest),
            )
        )

        root.add_child(
            QueryNode(
                "OR",
                self.builder.or_query(manifest),
            )
        )

        return root