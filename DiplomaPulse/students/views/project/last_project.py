from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from students.serializers.project.last_project import LastProjectSerializer, UserProjectSerializer
from students.views.base import StudentView


class GetLastProjectView(StudentView):
	serializer_class = LastProjectSerializer

	@swagger_auto_schema(
		operation_summary="Returns last project, if it exists",
		operation_description=(
			"This endpoint will return last project, if it exists. "
			"Call it with a valid JWT token in the header."
		),
		responses={
			status.HTTP_200_OK: UserProjectSerializer,
			status.HTTP_404_NOT_FOUND: openapi.Response(description="If there is no last project"),
		},
		tags=["students", "project"],
	)
	def get(self, request: Request, *args, **kwargs):
		serializer = LastProjectSerializer(
			data={
				"account_uuid": request.user.id,
			}
		)
		serializer.is_valid(raise_exception=True)
		project = serializer.create(serializer.validated_data)
		if not project:
			return Response(status=status.HTTP_404_NOT_FOUND)

		return Response(
			UserProjectSerializer(instance=project).data,
			status=status.HTTP_200_OK,
		)
