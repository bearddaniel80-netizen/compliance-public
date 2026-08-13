from .base_generator import CapabilityGenerator
from ...models import QueryNode

class ProjectionGenerator(CapabilityGenerator):

    def __init__(
        self,
        builder: QueryBuilder,
        scalar_registry: ScalarRegistry,
    ):
        self.builder = builder
        self.scalar_registry = scalar_registry

    def generate(
        self,
        manifest,
    ) -> QueryNode:

        root = QueryNode(
            name="projection",
        )

        #
        # SELECT *
        #

        select_star = QueryNode(
            name="star",
            query=self.builder.select_star(manifest),
        )

        # root.add_child(select_star)

        #
        # SELECT field1, field2
        #

        fields = QueryNode(
            name="fields",
            query=self.builder.select_fields(
                manifest,
                manifest.schema.fields,
            ),
        )

        select_star.add_child(fields)

        #
        # SELECT field AS alias
        #

        aliases = QueryNode(
            name="aliases",
            query=self.builder.select_aliases(
                manifest,
            ),
        )

        fields.add_child(aliases)

        #
        # Scalar functions
        #

        aliases.add_child(
            self._generate_scalars(manifest)
        )

        root.chain(
            select_star,
            fields,
            aliases
        )

        return root

    def _generate_scalars(
        self,
        manifest,
    ) -> QueryNode:

        root = QueryNode(
            name="scalar_functions",
        )

        for field in manifest.schema.fields:

            scalars = (
                self.scalar_registry
                .supported_for(field.type)
            )

            for scalar in scalars:

                query = (
                    self.builder
                    .scalar_projection(
                        manifest,
                        scalar,
                        field,
                    )
                )

                root.add_child(
                    QueryNode(
                        name=(
                            f"{scalar.name}"
                            f"({field.name})"
                        ),
                        query=query,
                    )
                )

        return root