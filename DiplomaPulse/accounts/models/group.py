from __future__ import annotations
from typing import TYPE_CHECKING

from django.db import models
from .base import BaseModel

if TYPE_CHECKING:
    from .student import Student
    from .faculty import Faculty


class Group(BaseModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    faculty: "Faculty" = models.ForeignKey(
        "Faculty",
        on_delete=models.CASCADE,
        related_name="groups",
    )
    students: "models.QuerySet[Student]"

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "faculty")
