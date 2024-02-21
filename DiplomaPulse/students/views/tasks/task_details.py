from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from students.serializers.tasks.task_details import (
    GetTaskDetailsSerializer,
    TaskDetailsInputSerializer,
    TaskDetailsOutputSerializer,
)
from students.views.base import StudentView


class GetTaskDetails(StudentView):
    serializer_class = GetTaskDetailsSerializer

    @swagger_auto_schema(
        operation_summary="Returns details about the task",
        query_serializer=TaskDetailsInputSerializer,
        responses={
            status.HTTP_200_OK: TaskDetailsOutputSerializer,
            status.HTTP_404_NOT_FOUND: openapi.Response(description="Task not found"),
        },
        tags=["students", "tasks"],
    )
    def get(self, request: Request) -> Response:
        serializer = self.serializer_class(
            data={
                "account_uuid": request.user.id,
                "task_id": request.query_params.get("task_id", None),
            }
        )
        serializer.is_valid(raise_exception=True)
        output_serializer = serializer.create()
        return Response(output_serializer.data)
