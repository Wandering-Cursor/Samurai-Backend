from communication.models.message import Message
from core.serializers.models import ModelWithUUID


class MessageSerializer(ModelWithUUID):
	class Meta:
		model = Message
		fields = "__all__"
		read_only_fields = ("id", "created_at", "updated_at")
