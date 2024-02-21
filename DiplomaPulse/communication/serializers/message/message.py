from core.serializers.models import ModelWithUUID

from communication.models.message import Message


class MessageSerializer(ModelWithUUID):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
