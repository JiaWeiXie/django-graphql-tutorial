import datetime
import typing
import uuid

import strawberry
import strawberry_django
from django.db.models import QuerySet
from strawberry import relay
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
class Post(relay.Node):
    id: relay.NodeID[uuid.UUID]  # noqa: A003
    slug: str
    author: auth_types.User
    title: str
    content: str
    published_at: datetime.datetime | None
    published: bool | None
    tags: list["Tag"]
    categories: list["Category"]
    cover_image: strawberry.auto

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
class Comment(relay.Node):
    id: relay.NodeID[uuid.UUID]  # noqa: A003
    post: Post
    parent: typing.Optional["Comment"]
    author: auth_types.User | None
    content: str


@strawberry_django.type(
    blog_models.Tag,
    order=blog_orders.TagOrder,
    filters=blog_filters.TagFilter,
)
class Tag(relay.Node):
    id: relay.NodeID[uuid.UUID]  # noqa: A003
    name: str


@strawberry_django.type(blog_models.Category)
class Category(relay.Node):
    id: relay.NodeID[uuid.UUID]  # noqa: A003
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
    tags: list[relay.GlobalID]
    categories: list[relay.GlobalID]
    author: str = strawberry.field(description="Username of the author")


@strawberry_django.partial(blog_models.Post)
class PostInputPartial:
    id: relay.GlobalID  # noqa: A003
    slug: strawberry.auto
    title: strawberry.auto
    content: strawberry.auto
    tags: list[relay.GlobalID] | None
    categories: list[relay.GlobalID] | None
    published_at: datetime.datetime | None
    published: bool | None


@strawberry.interface
class FormError:
    field: str
    message: str


@strawberry.type
class ValidationError(FormError):
    pass


@strawberry.type
class InvalidChoiceError(FormError):
    value: str


@strawberry.type
class DuplicateError(FormError):
    pass


@strawberry.type
class CreatePostResult:
    post: Post | None = strawberry.UNSET
    errors: list[
        typing.Annotated[
            ValidationError | (InvalidChoiceError | DuplicateError),
            strawberry.union("FormValidationError"),
        ]
    ] | None = strawberry.field(default=None)
