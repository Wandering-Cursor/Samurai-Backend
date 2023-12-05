from __future__ import annotations

from django.db import models
from .base_user import BaseUser

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .faculty import Faculty


class Teacher(BaseUser):
    faculties: "models.QuerySet[Faculty]" = models.ManyToManyField(
        "Faculty",
        related_name="teachers",
    )
    contact_information = models.TextField(blank=True, null=True)
