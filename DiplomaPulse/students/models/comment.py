from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from ._base import BaseModel


class Comment(BaseModel):
	file = models.FileField(upload_to="comments", blank=True, null=True, verbose_name=_("file"))
	text = models.TextField(default="", blank=True, verbose_name=_("text content"))

	author = models.ForeignKey(
		"accounts.BaseUser",
		related_name="comments",
		on_delete=models.CASCADE,
		verbose_name=_("author"),
	)

	def clean(self):
		super().clean()

		if not self.text and not self.file:
			raise ValidationError("Comment should have either text or file")

	class Meta:
		verbose_name = _("Comment")
		verbose_name_plural = _("Comments")
		ordering = ["-created_at"]

	def __str__(self):
		return f"Comment by {self.author}: '{self.text[:20]}...' at {self.created_at} "
