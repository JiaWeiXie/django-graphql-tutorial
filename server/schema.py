import strawberry
import strawberry.tools

from server.app.authentication.graph import mutations as auth_mutations
from server.app.authentication.graph import queries as auth_queries
from server.app.blog.graph import mutations as blog_mutations
from server.app.blog.graph import queries as blog_queries

__all__ = ("schema",)


query = strawberry.tools.merge_types(
    "Query",
    (
        blog_queries.Query,
        auth_queries.Query,
    ),
)
mutation = strawberry.tools.merge_types(
    "Mutation",
    (
        blog_mutations.Mutation,
        auth_mutations.Mutation,
    ),
)


schema = strawberry.Schema(query=query, mutation=mutation)
