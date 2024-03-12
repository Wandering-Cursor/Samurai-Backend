from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


def get_id_field() -> models.UUIDField:
    return models.UUIDField(primary_key=True, default=uuid4, editable=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated at"),
    )

    class Meta:
        abstract = True
