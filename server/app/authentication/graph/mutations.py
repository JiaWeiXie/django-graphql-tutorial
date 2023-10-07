import typing

import strawberry
import strawberry_django
import strawberry_django.auth
import strawberry_django.mutations
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from strawberry.types import Info
from strawberry.utils.str_converters import to_camel_case
from strawberry_django.fields.types import OperationInfo, OperationMessage
from strawberry_django.mutations.fields import DjangoCreateMutation
from strawberry_django.optimizer import DjangoOptimizerExtension

from server.app.authentication.forms import UserEditForm
from server.app.authentication.graph import types as auth_types

__all__ = ("Mutation",)


if typing.TYPE_CHECKING:
    from django.contrib.auth.base_user import AbstractBaseUser


class UserEditMutation(DjangoCreateMutation):
    def _handle_errors(
        self,
        errors: dict[str, list[ValidationError]],
    ) -> typing.Iterator[OperationMessage]:
        kind = OperationMessage.Kind.VALIDATION
        for field, field_errors in errors.items():
            for err in field_errors:
                yield OperationMessage(
                    kind=kind,
                    field=to_camel_case(field) if field != NON_FIELD_ERRORS else None,
                    message=err.message % err.params if err.params else err.message,
                    code=getattr(err, "code", None),
                )

    def create(
        self,
        data: dict[str, typing.Any],
        *,
        info: Info,
    ) -> typing.Union["AbstractBaseUser", "OperationInfo"]:
        model = typing.cast(type["AbstractBaseUser"], self.django_model)
        username = data.get("username")
        obj = model.objects.get(username=username)
        form = UserEditForm(data, instance=obj)
        if not form.is_valid():
            return OperationInfo(
                messages=list(self._handle_errors(form.errors.as_data())),
            )

        with DjangoOptimizerExtension.disabled():
            return form.save()


user_edit_mutation = (
    strawberry_django.mutations.create if typing.TYPE_CHECKING else UserEditMutation
)


@strawberry.type
class Mutation:
    user_register: auth_types.User = strawberry_django.auth.register(
        auth_types.UserRegisterInput,
        handle_django_errors=True,
    )
    user_edit: auth_types.User = user_edit_mutation(
        auth_types.UserEditInput,
        handle_django_errors=True,
    )
    login: auth_types.User = strawberry_django.auth.login()  # type: ignore
    logout: bool = strawberry_django.auth.logout()  # type: ignore
