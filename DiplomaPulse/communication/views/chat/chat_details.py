from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response

from communication.serializers.chat.chat import (
    ChatSerializer,
)
from communication.serializers.chat.details import ChatDetailsInputSerializer, ChatDetailsSerializer
from communication.views.base import CommunicationView


class ChatDetailsView(CommunicationView):
    serializer_class = ChatDetailsSerializer

    @swagger_auto_schema(
        query_serializer=ChatDetailsInputSerializer,
        responses={200: openapi.Response("Chat details", ChatSerializer)},
        tags=["communication", "chat"],
        operation_description="Lists all chats for the user. Available for all authenticated users",
    )
    def get(self, request: Request) -> Response:
        serializer = self.serializer_class(
            data={
                "chat_id": request.query_params.get("chat_id", None),
                "account_uuid": request.user.id,
            },
        )
        serializer.is_valid(raise_exception=True)
        output_serializer = serializer.create(serializer.validated_data)

        if not isinstance(output_serializer, ChatSerializer):
            raise ValueError("Output serializer not set")

        return Response(output_serializer.data)
