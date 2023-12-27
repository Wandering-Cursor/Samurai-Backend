from django.core.exceptions import ValidationError
from django.db import models

from ._base import BaseModel


class Comment(BaseModel):
	file = models.FileField(upload_to="comments", blank=True, null=True)
	text = models.TextField(default="", blank=True)

	author = models.ForeignKey(
		"accounts.BaseUser",
		related_name="comments",
		on_delete=models.CASCADE,
	)

	def clean(self):
		super().clean()

		if not self.text and not self.file:
			raise ValidationError("Comment should have either text or file")

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"Comment by {self.author}: '{self.text[:20]}...' at {self.created_at} "
