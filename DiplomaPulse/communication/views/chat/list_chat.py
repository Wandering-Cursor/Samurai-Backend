from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response

from communication.serializers.chat.list_chat import (
    ListChatInputSerializer,
    ListChatOutputSerializer,
    ListChatSerializer,
)
from communication.views.base import CommunicationView


class ListChatView(CommunicationView):
    serializer_class = ListChatSerializer

    @swagger_auto_schema(
        query_serializer=ListChatInputSerializer,
        responses={200: openapi.Response("List of chats", ListChatOutputSerializer)},
        tags=["communication", "chat"],
        operation_description="Lists all chats for the user. Available for all authenticated users",
    )
    def get(self, request: Request) -> Response:
        serializer = self.serializer_class(
            data=request.query_params,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        output_serializer = serializer.create(serializer.validated_data)

        if not isinstance(output_serializer, ListChatOutputSerializer):
            raise ValueError("Output serializer not set")

        return Response(output_serializer.data)
