import strawberry
import strawberry.tools

from server.app.blog.graph import mutations as blog_mutations
from server.app.blog.graph import queries as blog_queries

__all__ = ("schema",)


query = strawberry.tools.merge_types(
    "Query",
    (blog_queries.Query,),
)
mutation = strawberry.tools.merge_types(
    "Mutation",
    (blog_mutations.Mutation,),
)


schema = strawberry.Schema(query=query, mutation=mutation)
