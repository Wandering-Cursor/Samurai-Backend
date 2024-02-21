from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from ._base import BaseModel


class Comment(BaseModel):
    file = models.FileField(
        upload_to="comments",
        blank=True,
        null=True,
        verbose_name=_("file"),
    )
    text = models.TextField(
        default="",
        blank=True,
        null=True,
        verbose_name=_("text content"),
    )

    author = models.ForeignKey(
        "accounts.BaseUser",
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name=_("author"),
    )

    def clean(self) -> None:
        super().clean()

        if not self.text and not self.file:
            raise ValidationError("Comment should have either text or file")
        if self.text and self.file:
            raise ValidationError("Comments cannot have text AND file fields")

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Comment by {self.author}: '{str(self.text)[:20]}...' at {self.created_at} "
