from accounts.serializers.account.account_info import ShortBaseUserInfoSerializer
from core.serializers.models import ModelWithUUID
from rest_framework import serializers

from communication.models.chat import Chat
from communication.serializers.message.message import MessageSerializer


class ChatSerializer(ModelWithUUID):
    users = ShortBaseUserInfoSerializer(many=True)
    users_count = serializers.IntegerField()
    last_message = MessageSerializer(required=False, allow_null=True)

    class Meta:
        model = Chat
        fields = [
            "id",
            "name",
            "users",
            "users_count",
            "last_message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")


class ChatSerializerTrimmed(ChatSerializer):
    """A serializer for chat model, that trims users to 3 users"""

    users = ShortBaseUserInfoSerializer(
        many=True,
        source="trimmed_users",
        help_text="Shows only last 3 users of chat to reduce response size",
    )


class ChatFinderMixin:
    """All serializers using this Mixin must have a property `user`"""

    chat = None

    def validate_chat_id(self, chat_id: str) -> str:
        """Validates chat ID"""
        try:
            self.chat = Chat.objects.filter(users__id=self.user.id).get(id=chat_id)
        except Chat.DoesNotExist as e:
            raise serializers.ValidationError("Chat not found") from e

        return chat_id
