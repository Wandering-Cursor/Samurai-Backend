from rest_framework import serializers

from accounts.serializers.account.account_info import ShortBaseUserInfoSerializer
from communication.models.chat import Chat
from core.serializers.models import ModelWithUUID


class ChatSerializer(ModelWithUUID):
	users = ShortBaseUserInfoSerializer(many=True)
	users_count = serializers.IntegerField(read_only=True)

	class Meta:
		model = Chat
		fields = "__all__"
		read_only_fields = ("id", "created_at", "updated_at")


class ChatSerializerTrimmed(ChatSerializer):
	"""A serializer for chat model, that trims users to 3 users"""

	users = ShortBaseUserInfoSerializer(many=True, source="trimmed_users")
