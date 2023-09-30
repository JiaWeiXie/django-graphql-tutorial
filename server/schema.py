import strawberry
import strawberry.tools

from server.app.blog.graph import queries as blog_queries

__all__ = ("schema",)


query = strawberry.tools.merge_types(
    "Query",
    (blog_queries.Query,),
)


schema = strawberry.Schema(query=query)
