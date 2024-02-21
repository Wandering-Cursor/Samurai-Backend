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
        "communication.Message", related_name="chats", blank=True
    )

    @property
    def trimmed_users(self) -> list[BaseUser]:
        return self.users.all()[:3]

    @property
    def users_count(self) -> int:
        return self.users.count()

    @property
    def last_message(self) -> Message | None:
        return self.messages.last()

    @property
    def last_messages(self) -> list[Message]:
        return self.messages.all()[:3]

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"
        ordering = ["-updated_at"]
