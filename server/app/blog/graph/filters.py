import typing

import strawberry
import strawberry_django
from django.db.models import Q, QuerySet

from server.app.blog import models as blog_models

__all__ = (
    "PostFilter",
    "TagFilter",
)


@strawberry.input
class TitleFilterLookup:
    contains: str | None = strawberry.UNSET
    in_list: list[str] | None = strawberry.UNSET


@strawberry_django.filter(blog_models.Post)
class PostFilter:
    id: strawberry.auto  # noqa: A003
    slug: strawberry.auto
    tags: typing.Optional["TagFilter"]
    title: TitleFilterLookup | None
    search: str | None

    def filter_search(
        self,
        queryset: QuerySet[blog_models.Post],
    ) -> QuerySet[blog_models.Post]:
        if self.search:
            queryset = queryset.filter(
                Q(title__icontains=self.search)
                | Q(content__icontains=self.search)
                | Q(tags__name__icontains=self.search)
                | Q(categories__name__icontains=self.search),
            )

        return queryset


@strawberry_django.filter(blog_models.Tag, lookups=True)
class TagFilter:
    name: strawberry.auto
