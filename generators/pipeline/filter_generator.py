from .base_generator import CapabilityGenerator
from ...models import QueryNode

class FilterGenerator(CapabilityGenerator):

    def __init__(
        self,
        builder: QueryBuilder,
        operator_registry: OperatorRegistry,
    ):
        self.builder = builder
        self.operator_registry = operator_registry

    def generate(
        self,
        manifest,
    ) -> QueryNode:

        root = QueryNode(
            name="where",
        )

        #
        # One subtree per field
        #

        for field in manifest.schema.fields:

            field_node = QueryNode(
                name=field.name,
            )

            root.add_child(field_node)

            self._generate_field(
                manifest,
                field,
                field_node,
            )

        return root

    def _generate_field(
        self,
        manifest,
        field,
        parent,
    ):

        operators = (
            self.operator_registry
            .supported_for(field.type)
        )

        for operator in operators:

            query = self.builder.where(
                manifest,
                field,
                operator,
            )

            node = QueryNode(
                name=operator.name,
                query=query,
            )

            parent.add_child(node)