from rest_framework import serializers


class ChatDetailsInputSerializer(serializers.Serializer):
    chat_id = serializers.UUIDField(help_text="Chat ID", required=True)


# class ChatDetailsSerializer(ChatDetailsSerializer, Chat)
