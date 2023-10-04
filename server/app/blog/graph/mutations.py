import typing
import uuid

import strawberry
import strawberry_django
from django.utils import timezone
from strawberry_django import mutations

from server.app.blog import models as blog_models
from server.app.blog.graph import types as blog_types


@strawberry.type
class Mutation:
    create_post: blog_types.Post = mutations.create(blog_types.PostInput)
    update_post: blog_types.Post = mutations.update(blog_types.PostInputPartial)
    delete_post: blog_types.Post = mutations.delete(blog_types.PostIdInput)

    @strawberry_django.input_mutation(handle_django_errors=True)
    def publish_post(self, id: uuid.UUID) -> blog_types.Post:  # noqa: A002
        post = blog_models.Post.objects.get(pk=id)
        if not post.published:
            post.published = True
            post.published_at = timezone.now()
            post.save()
        return typing.cast(blog_types.Post, post)
