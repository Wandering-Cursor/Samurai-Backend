from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from accounts.models import BaseUser

from django.db import models

from ._base import BaseModel


class Message(BaseModel):
	from_user: BaseUser = models.ForeignKey(
		"accounts.BaseUser", related_name="sent_messages", on_delete=models.CASCADE
	)

	text = models.TextField(null=True, blank=True)
	file = models.FileField(upload_to="messages/", null=True, blank=True)

	read_by: models.ManyToManyField[BaseUser] = models.ManyToManyField(
		"accounts.BaseUser", related_name="read_messages"
	)

	class Meta:
		verbose_name = "Message"
		verbose_name_plural = "Messages"
		ordering = ["-created_at"]
