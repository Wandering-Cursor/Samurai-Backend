from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response

from communication.serializers.chat.leave_chat import (
    LeaveChatInputSerializer,
    LeaveChatOutputSerializer,
    LeaveChatSerializer,
)
from communication.views.base import CommunicationView


class LeaveChatView(CommunicationView):
    serializer_class = LeaveChatSerializer

    @swagger_auto_schema(
        request_body=LeaveChatInputSerializer,
        responses={
            200: openapi.Response(
                description="Operation was successful",
                schema=LeaveChatOutputSerializer,
            )
        },
        operation_description="Leave a chat. If no members are left in a chat - it will be removed",
        tags=["communication", "chat"],
    )
    def delete(self, request: Request) -> Response:
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        output_serializer = serializer.create(request.data)
        return Response(output_serializer.data)
