from accounts.serializers.account.mixin import AccountSerializerMixIn
from rest_framework import serializers

from communication.serializers.chat.chat import ChatFinderMixin


class LeaveChatInputSerializer(serializers.Serializer):
    chat_id = serializers.UUIDField(
        help_text="ID of a chat from which you want to leave",
        required=True,
    )


class LeaveChatOutputSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        help_text="Status of the operation", required=True, choices=["success", "error"]
    )


class LeaveChatSerializer(AccountSerializerMixIn, ChatFinderMixin, LeaveChatInputSerializer):
    def create(self, _: dict) -> LeaveChatOutputSerializer:
        if not self.chat:
            raise ValueError("Chat not found")

        self.chat.users.remove(self.user)
        if self.chat.users.count() == 0:
            self.chat.delete()

        output_serializer = LeaveChatOutputSerializer(data={"status": "success"})
        output_serializer.is_valid(raise_exception=True)

        return output_serializer
