from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from DiplomaPulse.views import AuthenticatedApiView
from accounts.serializers.account.account_info import (
    AccountInfoSerializer,
    AllUsersInfoSerializer,
)


class AccountInfoView(AuthenticatedApiView):
    @swagger_auto_schema(
        operation_summary="Get information about the current user",
        operation_description="This endpoint will return information about the current user. Call it with a valid JWT token in the header.",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Response with details about the user. Please, keep in mind that you will get only one of provided responses (value only, without nesting)",
                schema=AllUsersInfoSerializer,
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="If you call this endpoint without a valid JWT token in the header, you will get this response.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            default="Authentication credentials were not provided.",
                            description="Error message",
                        ),
                    },
                ),
            ),
        },
        tags=["account"],
    )
    def get(self, request: Request) -> Response:
        serializer = AccountInfoSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
