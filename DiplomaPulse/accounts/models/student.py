from __future__ import annotations
from typing import TYPE_CHECKING

from django.db import models
from .base_user import BaseUser

if TYPE_CHECKING:
    from .group import Group


class Student(BaseUser):
    group: "Group" = models.ForeignKey(
        "Group",
        on_delete=models.CASCADE,
        related_name="students",
    )
