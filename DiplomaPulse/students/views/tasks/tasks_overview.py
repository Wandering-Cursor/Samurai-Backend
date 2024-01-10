from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from students.serializers.tasks.tasks_overview import (
	GetTasksOverviewSerializer,
	TasksOverviewInputSerializer,
	TasksOverviewOutputSerializer,
)
from students.views.base import StudentView


class GetTasksOverview(StudentView):
	serializer_class = GetTasksOverviewSerializer

	@swagger_auto_schema(
		operation_summary="Returns statistics of a project",
		operation_description=(
			"If you don't pass project_id - returns stats " "of the most recent project"
		),
		query_serializer=TasksOverviewInputSerializer,
		responses={
			status.HTTP_200_OK: TasksOverviewOutputSerializer,
			status.HTTP_404_NOT_FOUND: openapi.Response(description="If there is no last project"),
		},
		tags=["students", "tasks"],
	)
	def get(self, request: Request):
		serializer = self.serializer_class(
			data={
				"account_uuid": request.user.id,
				"project_id": request.query_params.get("project_id", None),
			}
		)
		serializer.is_valid(raise_exception=True)
		overview_serializer, recent_tasks_serializer = serializer.create()
		overview_serializer.is_valid(raise_exception=True)

		output_serializer = TasksOverviewOutputSerializer(
			data={
				"statistics": overview_serializer.data,
				"recent": recent_tasks_serializer.data,
			}
		)
		output_serializer.is_valid(raise_exception=True)

		return Response(data=output_serializer.data)
