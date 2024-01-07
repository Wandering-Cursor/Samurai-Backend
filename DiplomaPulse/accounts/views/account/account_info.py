from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.serializers.account.account_info import AccountInfoSerializer, AllUsersInfoSerializer
from DiplomaPulse.views import AuthenticatedApiView


class AccountInfoView(AuthenticatedApiView):
	@swagger_auto_schema(
		operation_summary="Get information about the user",
		operation_description=(
			"This endpoint will return information about the user. "
			"Call it with a valid JWT token in the header. "
			"If you pass the account_id parameter - it will try to fetch data for that user"
		),
		query_serializer=AccountInfoSerializer,
		responses={
			status.HTTP_200_OK: openapi.Response(
				description=(
					"Response with details about the user. Please, keep in mind that you "
					"will get only one of provided responses (value only, without nesting)"
				),
				schema=AllUsersInfoSerializer,
			),
			status.HTTP_401_UNAUTHORIZED: openapi.Response(
				description=(
					"If you call this endpoint without a valid JWT"
					"token in the header, you will get this response."
				),
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
		serializer = AccountInfoSerializer(
			instance=request.user,
			data=request.query_params,
		)
		serializer.is_valid(raise_exception=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
