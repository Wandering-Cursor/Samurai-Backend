from core.serializers.fields import Base64Field
from django.core.files.base import ContentFile
from django.db.transaction import atomic
from django.utils.crypto import get_random_string
from rest_framework import serializers
from students.serializers.comments.comment import validate_comment_content

from communication.models.message import Message
from communication.serializers.chat.chat import UserChatFinderMixin
from communication.serializers.message.message import MessageSerializer


class SendMessageInputSerializer(serializers.Serializer):
    """
    Message Input. Takes chat_id, in which message will be sent.
    And text, or a file.
    """

    chat_id = serializers.UUIDField()
    text = serializers.CharField(
        required=False,
        allow_blank=False,
        allow_null=True,
        trim_whitespace=False,  # I believe it's cool :)
    )
    file_name = serializers.CharField(
        required=False,
        allow_null=True,
    )
    file_content = Base64Field(
        required=False,
        allow_null=True,
    )


class SendMessageOutputSerializer(MessageSerializer):
    pass


class AddCommentSerializer(SendMessageInputSerializer, UserChatFinderMixin):
    def validate(self, args: dict) -> dict:
        return validate_comment_content(super().validate(args))

    def create(self, validated_data: dict) -> Message:
        with atomic():
            file = None
            if file_content := validated_data.get("file_content"):
                file_name = validated_data.get("file_name")
                file_name = f"{get_random_string(length=16)}_{file_name}"

                file = ContentFile(
                    content=file_content,
                    name=file_name,
                )

            message = Message.objects.create(
                file=file,
                text=validated_data.get("text"),
                from_user=self.user,
            )
            message.read_by.add(self.user)

            self.chat.messages.add(message)

            return message
