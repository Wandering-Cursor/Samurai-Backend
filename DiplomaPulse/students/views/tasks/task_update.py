from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from students.serializers.tasks.task import TaskNotFound, TaskSerializer
from students.serializers.tasks.task_update import (
	UpdateTaskForbiddenSerializer,
	UpdateTaskInputSerializer,
	UpdateTaskSerializer,
)
from students.views.base import StudentView


class UpdateTask(StudentView):
	serializer_class = UpdateTaskSerializer

	@swagger_auto_schema(
		operation_summary="Allows to change status of a task (as a Student)",
		request_body=UpdateTaskInputSerializer,
		responses={
			status.HTTP_200_OK: TaskSerializer,
			status.HTTP_403_FORBIDDEN: UpdateTaskForbiddenSerializer,
			status.HTTP_404_NOT_FOUND: TaskNotFound,
		},
		tags=["students", "tasks"],
	)
	def patch(self, request: Request):
		try:
			serializer = self.serializer_class(
				data={
					"account_uuid": request.user.id,
					"task_id": request.data.get("task_id", None),
					"state": request.data.get("state", None),
				}
			)
			serializer.is_valid(raise_exception=True)

			task = serializer.create(serializer.validated_data)
		except Exception as e:
			arg: UpdateTaskForbiddenSerializer | TaskNotFound = e.args[0]
			arg.is_valid(raise_exception=True)
			return Response(data=arg.data, status=arg.data["code"])

		return Response(data=TaskSerializer(instance=task).data)
