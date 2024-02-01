from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from students.serializers.comments.comment import CommentNotFound
from students.serializers.comments.delete_comment import (
	DeleteCommentInputSerializer,
	DeleteCommentOutputSerializer,
	DeleteCommentSerializer,
)
from students.views.base import StudentView


class DeleteCommentView(StudentView):
	serializer_class = DeleteCommentSerializer

	@swagger_auto_schema(
		request_body=DeleteCommentInputSerializer,
		responses={
			HTTP_200_OK: DeleteCommentOutputSerializer,
			HTTP_404_NOT_FOUND: CommentNotFound,
		},
		tags=["students", "comments"],
	)
	def delete(self, request: Request):
		try:
			serializer = self.serializer_class(
				data={
					"account_uuid": request.user.id,
					"comment_id": request.data.get("comment_id", None),
				}
			)
			serializer.is_valid(raise_exception=True)
			output_serializer = serializer.delete()
		except Exception as e:
			error_serializer = e.args[0]
			if not isinstance(error_serializer, Serializer):
				raise e

			error_serializer.is_valid(raise_exception=True)
			return Response(error_serializer.data, status=error_serializer.data["code"])

		return Response(data=output_serializer.data)
