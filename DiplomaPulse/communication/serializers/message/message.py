from core.serializers.models import ModelWithUUID
from rest_framework import serializers

from communication.models.message import Message


class MessageSerializer(ModelWithUUID):
    message_id = serializers.UUIDField(
        help_text="Message ID",
    )

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ("message_id", "created_at", "updated_at")
