from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from accounts.models import BaseUser
	from .message import Message

from django.db import models

from communication.utils.randomizer import get_random_pass_name

from ._base import BaseModel


class Chat(BaseModel):
	"""
	Model for chat, used to send messages between userss
	"""

	name = models.CharField(max_length=255, default=get_random_pass_name)
	users: models.ManyToManyField[BaseUser] = models.ManyToManyField(
		"accounts.BaseUser", related_name="chats"
	)
	messages: models.ManyToManyField[Message] = models.ManyToManyField(
		"communication.Message", related_name="chats"
	)

	@property
	def last_message(self):
		return self.messages.last()
