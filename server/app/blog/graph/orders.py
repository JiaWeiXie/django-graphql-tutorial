import strawberry
import strawberry_django

from server.app.blog import models as blog_models

__all__ = (
    "PostOrder",
    "TagOrder",
)


@strawberry_django.order(blog_models.Post)
class PostOrder:
    published_at: strawberry.auto


@strawberry_django.order(blog_models.Tag)
class TagOrder:
    name: strawberry.auto
