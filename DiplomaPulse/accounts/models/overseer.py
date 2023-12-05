from __future__ import annotations
from typing import TYPE_CHECKING

from django.db import models
from .base_user import BaseUser

if TYPE_CHECKING:
    from .faculty import Faculty


class Overseer(BaseUser):
    faculty: "Faculty" = models.ForeignKey(
        "Faculty", on_delete=models.CASCADE, related_name="overseers"
    )
