from accounts.serializers.account.mixin import AccountSerializerMixIn
from django.core.paginator import Paginator
from rest_framework import serializers

from communication.models.chat import Chat
from communication.serializers.chat.chat import ChatSerializerTrimmed


class ListChatInputSerializer(serializers.Serializer):
    page = serializers.IntegerField(
        default=1,
        min_value=1,
    )
    page_size = serializers.IntegerField(
        default=25,
        min_value=1,
    )
    chat_name = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="Pass chat name, or it's part to filter chats",
    )


class ListChatOutputSerializer(serializers.Serializer):
    pages = serializers.IntegerField(min_value=1, default=1)
    content = ChatSerializerTrimmed(many=True)


class ListChatSerializer(AccountSerializerMixIn, ListChatInputSerializer):
    output_serializer = None

    def validate(self, attrs: dict) -> dict:
        attrs = super().validate(attrs)

        page = attrs["page"]
        page_size = attrs["page_size"]

        queryset = Chat.objects.filter(
            users__id=self.user.id,
        )

        if chat_name := attrs.get("chat_name", None):
            queryset = queryset.filter(name__icontains=chat_name)

        paginator = Paginator(
            object_list=queryset,
            per_page=page_size,
        )

        chats_list: list[Chat] = list(paginator.get_page(page))
        chats_list_serializer = ChatSerializerTrimmed(instance=chats_list, many=True)
        total_pages = paginator.num_pages

        self.output_serializer = ListChatOutputSerializer(
            data={
                "pages": total_pages,
                "content": chats_list_serializer.data,
            }
        )

        self.output_serializer.is_valid(raise_exception=True)

        return attrs

    def create(self, _: dict) -> ListChatOutputSerializer:
        if not isinstance(self.output_serializer, ListChatOutputSerializer):
            raise ValueError("Output serializer not set")

        return self.output_serializer
