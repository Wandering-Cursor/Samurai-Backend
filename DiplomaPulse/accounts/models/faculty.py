from __future__ import annotations
from typing import TYPE_CHECKING

from django.db import models
from .base import BaseModel

if TYPE_CHECKING:
    from .group import Group


class Faculty(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    groups: "models.QuerySet[Group]"

    def __str__(self):
        return self.name
