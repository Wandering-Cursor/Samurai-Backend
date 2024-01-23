from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from students.serializers.comments.list_comments import (
	ListCommentsInputSerializer,
	ListCommentsOutputSerializer,
	ListCommentsSerializer,
)
from students.serializers.tasks.task import TaskNotFound
from students.views.base import StudentView


class ListCommentsView(StudentView):
	serializer_class = ListCommentsSerializer

	@swagger_auto_schema(
		query_serializer=ListCommentsInputSerializer,
		responses={
			HTTP_200_OK: ListCommentsOutputSerializer,
			HTTP_404_NOT_FOUND: TaskNotFound,
		},
		tags=["students", "comments"],
	)
	def get(self, request: Request):
		serializer = self.serializer_class(
			data={
				"account_uuid": request.user.id,
				"task_id": request.query_params.get("task_id", None),
				"page": request.query_params.get("page", None),
				"page_size": request.query_params.get("page_size", None),
			}
		)
		serializer.is_valid(raise_exception=True)
		output_serializer = serializer.create()

		return Response(data=output_serializer.data)
