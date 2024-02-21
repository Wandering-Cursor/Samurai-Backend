from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response

from communication.serializers.chat.create_chat import (
    CreateChatInputSerializer,
    CreateChatOutputSerializer,
    CreateChatSerializer,
)
from communication.views.base import CommunicationView


class CreateChatView(CommunicationView):
    serializer_class = CreateChatSerializer

    @swagger_auto_schema(
        request_body=CreateChatInputSerializer,
        responses={
            201: openapi.Response("Chat was created successfully", CreateChatOutputSerializer)
        },
        tags=["communication", "chat"],
        operation_description="Creates a new chat. Available for all authenticated users",
    )
    def post(self, request: Request) -> Response:
        if not isinstance(request.data, dict):
            raise ValueError("Supplied data is invalid")

        data = request.data.copy()
        data.update({"account_uuid": request.user.id})

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        output_serializer = serializer.create(serializer.validated_data)

        if not isinstance(output_serializer, CreateChatOutputSerializer):
            raise ValueError("Output serializer not set")

        return Response(output_serializer.data, status=201)
