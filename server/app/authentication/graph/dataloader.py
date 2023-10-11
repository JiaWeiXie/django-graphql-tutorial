import typing

from django.contrib.auth import get_user_model, models
from graphql_sync_dataloaders import SyncDataLoader

__all__ = ("user_loader",)


USER_MODEL = get_user_model()


def _load_users(keys: list[int]) -> list[models.AbstractUser]:
    return typing.cast(
        list[models.AbstractUser],
        list(USER_MODEL.objects.prefetch_related("posts").filter(id__in=keys)),
    )


user_loader = SyncDataLoader(_load_users)
