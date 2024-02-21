from accounts.serializers.account.mixin import AccountSerializerMixIn
from rest_framework import serializers

from communication.serializers.chat.chat import ChatFinderMixin, ChatSerializer


class ChatDetailsInputSerializer(serializers.Serializer):
    chat_id = serializers.UUIDField(help_text="Chat ID", required=True)


class ChatDetailsSerializer(AccountSerializerMixIn, ChatFinderMixin, ChatDetailsInputSerializer):
    def create(self, _: dict) -> ChatSerializer:
        chat = self.chat
        return ChatSerializer(chat)
