from communication.models.chat import Chat
from core.serializers.models import ModelWithUUID


class ChatSerializer(ModelWithUUID):
	class Meta:
		model = Chat
		fields = "__all__"
		read_only_fields = ("id", "created_at", "updated_at")
