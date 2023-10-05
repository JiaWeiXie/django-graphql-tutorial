import typing
import uuid

import strawberry
import strawberry_django
from django.core.exceptions import ValidationError
from django.utils import timezone
from strawberry.utils.str_converters import to_camel_case
from strawberry_django import mutations

from server.app.blog import forms as blog_forms
from server.app.blog import models as blog_models
from server.app.blog.graph import types as blog_types


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
    update_post: blog_types.Post = mutations.update(blog_types.PostInputPartial)
    delete_post: blog_types.Post = mutations.delete(blog_types.PostIdInput)

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

    @strawberry_django.input_mutation(handle_django_errors=True)
    def publish_post(self, id: uuid.UUID) -> blog_types.Post:  # noqa: A002
        post = blog_models.Post.objects.get(pk=id)
        if not post.published:
            post.published = True
            post.published_at = timezone.now()
            post.save()
        return typing.cast(blog_types.Post, post)
