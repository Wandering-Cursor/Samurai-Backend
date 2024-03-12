from rest_framework import serializers

from communication.serializers.chat.chat import ChatSerializer, UserChatFinderMixin


class ChatDetailsInputSerializer(serializers.Serializer):
    chat_id = serializers.UUIDField(help_text="Chat ID", required=True)


class ChatDetailsSerializer(UserChatFinderMixin, ChatDetailsInputSerializer):
    def create(self, _: dict) -> ChatSerializer:
        chat = self.chat
        return ChatSerializer(chat)
