import strawberry_django

from server.app.blog import models as blog_models

__all__ = (
    "Post",
    "Comment",
    "Tag",
    "Category",
)


@strawberry_django.type(blog_models.Post, fields="__all__")
class Post:
    pass


@strawberry_django.type(blog_models.Comment, fields="__all__")
class Comment:
    pass


@strawberry_django.type(blog_models.Tag, fields=["name"])
class Tag:
    pass


@strawberry_django.type(
    blog_models.Category,
    exclude=["created_at", "motified_at"],
)
class Category:
    pass
