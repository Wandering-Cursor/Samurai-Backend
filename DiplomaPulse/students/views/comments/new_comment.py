from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from students.serializers.comments.comment import BadCommentRequest
from students.serializers.comments.new_comment import (
	AddCommentSerializer,
	NewCommentInputSerializer,
	NewCommentOutputSerializer,
)
from students.serializers.tasks.task import TaskNotFound
from students.views.base import StudentView


class AddCommentView(StudentView):
	serializer_class = AddCommentSerializer

	@swagger_auto_schema(
		request_body=NewCommentInputSerializer,
		responses={
			HTTP_201_CREATED: NewCommentOutputSerializer,
			HTTP_400_BAD_REQUEST: BadCommentRequest,
			HTTP_404_NOT_FOUND: TaskNotFound,
		},
		tags=["students", "comments"],
	)
	def post(self, request: Request):
		try:
			serializer = self.serializer_class(
				data={
					"account_uuid": request.user.id,
					"task_id": request.data.get("task_id", None),
					"file_name": request.data.get("file_name", None),
					"file_content": request.data.get("file_content", None),
					"text": request.data.get("text", None),
				}
			)
			serializer.is_valid(raise_exception=True)
			new_comment = serializer.create(serializer.validated_data)
		except Exception as e:
			error_serializer = e.args[0]
			if not isinstance(error_serializer, Serializer):
				raise e

			error_serializer.is_valid(raise_exception=True)
			return Response(error_serializer.data, status=error_serializer.data["code"])

		output_serializer = NewCommentOutputSerializer(new_comment)

		return Response(
			output_serializer.data,
			status=HTTP_201_CREATED,
		)
