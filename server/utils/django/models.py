import uuid

from django.db import models

__all__ = [
    "UUIDModel",
    "TimestampModel",
    "BaseModel",
]


class UUIDModel(models.Model):
    id = models.UUIDField(  # noqa: A003
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    class Meta:
        abstract = True


class TimestampModel(models.Model):
    created_at = models.DateTimeField("建立時間", auto_now_add=True, editable=False)
    motified_at = models.DateTimeField("修改時間", auto_now=True, editable=False)

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimestampModel):
    class Meta:
        abstract = True
