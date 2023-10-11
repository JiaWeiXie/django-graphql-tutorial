import strawberry
import strawberry.tools
from graphql_sync_dataloaders import DeferredExecutionContext
from strawberry_django.optimizer import DjangoOptimizerExtension

from server.app.authentication.graph import mutations as auth_mutations
from server.app.authentication.graph import queries as auth_queries
from server.app.blog.graph import mutations as blog_mutations
from server.app.blog.graph import queries as blog_queries
from server.app.blog.graph import subscriptions as blog_subscriptions

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
subscription = strawberry.tools.merge_types(
    "Subscription",
    (blog_subscriptions.Subscription,),
)


schema = strawberry.Schema(
    query=query,
    mutation=mutation,
    execution_context_class=DeferredExecutionContext,
    extensions=[DjangoOptimizerExtension],
)
ws_schema = strawberry.Schema(query=query, subscription=subscription)
