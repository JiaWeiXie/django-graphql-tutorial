import datetime
import typing
import uuid

import strawberry
import strawberry_django
from django.db.models import QuerySet
from strawberry.types import Info

from server.app.authentication.graph import types as auth_types
from server.app.blog import models as blog_models
from server.app.blog.graph import filters as blog_filters
from server.app.blog.graph import orders as blog_orders

__all__ = (
    "Post",
    "Comment",
    "Tag",
    "Category",
)


@strawberry_django.type(blog_models.Post)
class Post:
    id: uuid.UUID  # noqa: A003
    slug: str
    author: auth_types.User
    title: str
    content: str
    published_at: datetime.datetime | None
    published: bool | None
    tags: list["Tag"]
    categories: list["Category"]

    @strawberry_django.field
    def comments(self) -> list["Comment"]:
        return self.comment_set.all()  # type: ignore

    @classmethod
    def get_queryset(
        cls,
        queryset: QuerySet[blog_models.Post],
        info: Info,
        **kwargs: typing.Any,
    ) -> QuerySet[blog_models.Post]:
        return queryset.select_related("author").prefetch_related(
            "tags",
            "categories",
            "comment_set",
        )


@strawberry_django.type(blog_models.Comment)
class Comment:
    id: uuid.UUID  # noqa: A003
    post: Post
    parent: typing.Optional["Comment"]
    author: auth_types.User | None
    content: str


@strawberry_django.type(
    blog_models.Tag,
    order=blog_orders.TagOrder,
    filters=blog_filters.TagFilter,
)
class Tag:
    name: str


@strawberry_django.type(blog_models.Category)
class Category:
    id: uuid.UUID  # noqa: A003
    slug: str
    parent: typing.Optional["Category"]
    name: str

    @strawberry_django.field
    def path(self) -> str:
        return str(self)


@strawberry_django.input(blog_models.Post)
class PostInput:
    slug: str
    title: str
    content: str
    author: strawberry.auto
    tags: strawberry.auto
    categories: strawberry.auto


@strawberry_django.partial(blog_models.Post)
class PostInputPartial:
    id: strawberry.auto  # noqa: A003
    slug: strawberry.auto
    title: strawberry.auto
    content: strawberry.auto
    tags: strawberry.auto
    categories: strawberry.auto
    published_at: datetime.datetime | None
    published: bool | None


@strawberry_django.input(blog_models.Post)
class PostIdInput:
    id: strawberry.auto  # noqa: A003
