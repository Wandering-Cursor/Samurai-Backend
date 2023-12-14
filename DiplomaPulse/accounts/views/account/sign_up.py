from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from DiplomaPulse.views import PublicApiView
from accounts.serializers.account.sign_up import BaseUserSerializer, SignUpSerializer


class SignUpView(PublicApiView):
    serializer_class = SignUpSerializer

    @swagger_auto_schema(
        operation_summary="Create a new user",
        operation_description="When creating a new user - you have to provide a registration code, which was assigned to you by the admin. (You can get it from the admin or from the person who invited you to the platform).",
        request_body=SignUpSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="User was created successfully. Returning some information about the user.",
                schema=BaseUserSerializer,
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Invalid registration code was supplied. Could not find a user assigned to it.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "registration_code": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            default="Invalid registration code",
                            description="Description of the error with the registration code",
                        )
                    },
                ),
            ),
        },
        tags=["account"],
    )
    def post(self, request: Request):
        sign_up_serializer = SignUpSerializer(data=request.data)
        sign_up_serializer.is_valid(raise_exception=True)
        account_serializer = sign_up_serializer.create(
            sign_up_serializer.validated_data,
            return_representation=True,
        )
        return Response(
            account_serializer.data,
            status=status.HTTP_201_CREATED,
        )
