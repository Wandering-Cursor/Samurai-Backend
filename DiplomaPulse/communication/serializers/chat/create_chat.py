from accounts.serializers.account.account_info import UserUUID
from accounts.serializers.account.mixin import AccountSerializerMixIn
from django.db.transaction import atomic
from rest_framework import serializers

from communication.models.chat import Chat
from DiplomaPulse.logger import main_logger


class CreateChatInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False, allow_null=True)
    participants = UserUUID(required=False, many=True)


class CreateChatOutputSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Chat
        fields = ["id", "name"]
        read_only_fields = fields


class CreateChatSerializer(CreateChatInputSerializer, AccountSerializerMixIn):
    @atomic
    def create(self, validated_data: dict) -> CreateChatOutputSerializer:
        kwargs = {}

        if chat_name := validated_data.get("name"):
            kwargs["name"] = chat_name

        chat = Chat.objects.create(**kwargs)

        users = validated_data.get("participants", [])
        # Add the user who created the chat
        users.append(
            {
                "id": self.user.id,
            }
        )

        try:
            chat.users.set([user["id"] for user in users])
        except Exception as e:  # noqa: BLE001
            main_logger.error(f"Failed to set users for chat {chat.id=}: {e} - {users=}")
            raise serializers.ValidationError(
                detail={"participants": "Failed to set participants for chat"},
                code=400,
            ) from e

        output_serializer = CreateChatOutputSerializer(chat)

        if not isinstance(output_serializer, CreateChatOutputSerializer):
            raise ValueError("Output serializer not set")

        return output_serializer
