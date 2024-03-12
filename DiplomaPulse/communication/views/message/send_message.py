from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response

from communication.serializers.message.send_message import (
    AddCommentSerializer,
    SendMessageInputSerializer,
    SendMessageOutputSerializer,
)
from communication.views.base import CommunicationView


class SendMessageView(CommunicationView):
    @swagger_auto_schema(
        request_body=SendMessageInputSerializer,
        responses={200: openapi.Response("Sent message", SendMessageOutputSerializer)},
        tags=["communication", "message"],
    )
    def post(self, request: Request) -> Response:
        serializer = AddCommentSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        message = serializer.create(serializer.validated_data)
        return Response(SendMessageOutputSerializer(message).data)
