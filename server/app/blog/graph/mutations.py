import typing
import uuid

import strawberry
import strawberry_django
from django.core.exceptions import ValidationError
from django.utils import timezone
from strawberry.file_uploads import Upload
from strawberry.permission import BasePermission
from strawberry.types import Info
from strawberry.utils.str_converters import to_camel_case
from strawberry_django.permissions import (
    HasPerm,
    IsStaff,
)

from server.app.blog import forms as blog_forms
from server.app.blog import models as blog_models
from server.app.blog.graph import types as blog_types


class IsAuthor(BasePermission):
    message = "You must be the author of this post to perform this action."

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        data = kwargs["data"]
        post = data["id"].resolve_node_sync(info, ensure_type=blog_models.Post)
        user = info.context.request.user
        if post.author == user:
            return True
        return False


def _handle_form_errors(
    errors: dict[str, list[ValidationError]],
) -> typing.Iterator[
    blog_types.ValidationError
    | blog_types.InvalidChoiceError
    | blog_types.DuplicateError
]:
    for field, field_errors in errors.items():
        for err in field_errors:
            code = getattr(err, "code", "invalid")
            if code == "unique":
                yield blog_types.DuplicateError(
                    field=to_camel_case(field),
                    message=err.message % err.params if err.params else err.message,
                )
            elif code == "invalid_choice":
                yield blog_types.InvalidChoiceError(
                    field=to_camel_case(field),
                    message=err.message % err.params if err.params else err.message,
                    value=err.params["value"],
                )
            else:
                yield blog_types.ValidationError(
                    field=to_camel_case(field),
                    message=err.message % err.params if err.params else err.message,
                )


@strawberry.type
class Mutation:
    @strawberry_django.mutation(
        handle_django_errors=True,
        permission_classes=[IsAuthor],
    )
    def update_post(
        self,
        data: blog_types.PostInputPartial,
        info: Info,
    ) -> blog_types.Post:
        post = data.id.resolve_node_sync(info, ensure_type=blog_models.Post)
        input_data = vars(data)
        for field, value in input_data.items():
            if field in ("id", "tags", "categories"):
                continue

            if value and hasattr(post, field):
                setattr(post, field, value)

        post.save()
        if data.tags and isinstance(data.tags, list):
            tags = [
                tag_id.resolve_node_sync(info, ensure_type=blog_models.Tag)
                for tag_id in data.tags
            ]
            post.tags.set(tags)

        if data.categories and isinstance(data.categories, list):
            categories = [
                category_id.resolve_node_sync(info, ensure_type=blog_models.Category)
                for category_id in data.categories
            ]
            post.categories.set(categories)

        return typing.cast(blog_types.Post, post)

    @strawberry_django.mutation
    def create_post(self, data: blog_types.PostInput) -> blog_types.CreatePostResult:
        form = blog_forms.PostForm(vars(data))
        if not form.is_valid():
            return blog_types.CreatePostResult(
                post=None,
                errors=list(_handle_form_errors(form.errors.as_data())),
            )
        post = form.save()
        return blog_types.CreatePostResult(post=post)

    @strawberry_django.input_mutation(
        handle_django_errors=True,
        extensions=[
            HasPerm(["blog.publish_post", "blog.view_post"], any_perm=False),
            IsStaff(),
        ],
    )
    def publish_post(self, id: uuid.UUID) -> blog_types.Post:  # noqa: A002
        post = blog_models.Post.objects.get(pk=id)
        if not post.published:
            post.published = True
            post.published_at = timezone.now()
            post.save()
        return typing.cast(blog_types.Post, post)

    @strawberry_django.mutation(handle_django_errors=True)
    def upload_post_cover_image(
        self,
        post_id: uuid.UUID,
        file: Upload,
    ) -> blog_types.Post:
        post = blog_models.Post.objects.get(pk=post_id)
        post.cover_image = file  # type: ignore
        post.save()
        return typing.cast(blog_types.Post, post)
