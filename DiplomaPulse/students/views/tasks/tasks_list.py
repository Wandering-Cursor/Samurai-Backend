from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from students.serializers.tasks.tasks_list import (
    GetTasksListSerializer,
    TaskListInputSerializer,
    TasksListOutputSerializer,
)
from students.views.base import StudentView


class GetTasksList(StudentView):
    serializer_class = GetTasksListSerializer

    @swagger_auto_schema(
        operation_summary="Returns list of tasks for a project",
        operation_description=(
            "If you don't pass project_id - returns stats of the most recent project"
        ),
        query_serializer=TaskListInputSerializer,
        responses={
            status.HTTP_200_OK: TasksListOutputSerializer,
            status.HTTP_404_NOT_FOUND: openapi.Response(description="If there is no last project"),
        },
        tags=["students", "tasks"],
    )
    def get(self, request: Request) -> Response:
        serializer = self.serializer_class(
            data={
                "account_uuid": request.user.id,
                "project_id": request.query_params.get("project_id", None),
                "page": request.query_params.get("page"),
                "page_size": request.query_params.get("page_size"),
            }
        )
        serializer.is_valid(raise_exception=True)
        output_serializer = serializer.create()

        output_serializer.is_valid(raise_exception=True)

        return Response(data=output_serializer.data)
