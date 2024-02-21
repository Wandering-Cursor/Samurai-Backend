from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from students.serializers.comments.comment import BadCommentRequest, CommentNotFound
from students.serializers.comments.update_comment import (
    UpdateCommentInputSerializer,
    UpdateCommentOutputSerializer,
    UpdateCommentSerializer,
)
from students.views.base import StudentView


class UpdateCommentView(StudentView):
    serializer_class = UpdateCommentSerializer

    @swagger_auto_schema(
        request_body=UpdateCommentInputSerializer,
        responses={
            HTTP_200_OK: UpdateCommentOutputSerializer,
            HTTP_400_BAD_REQUEST: BadCommentRequest,
            HTTP_404_NOT_FOUND: CommentNotFound,
        },
        tags=["students", "comments"],
    )
    def put(self, request: Request) -> Response:
        try:
            serializer = self.serializer_class(
                data={
                    "account_uuid": request.user.id,
                    "comment_id": request.data.get("comment_id", None),
                    "file_name": request.data.get("file_name", None),
                    "file_content": request.data.get("file_content", None),
                    "text": request.data.get("text", None),
                }
            )
            serializer.is_valid(raise_exception=True)
            comment = serializer.update(serializer.comment, serializer.validated_data)
        except Exception as e:  # noqa: BLE001
            error_serializer = e.args[0]
            if not isinstance(error_serializer, Serializer):
                raise e

            error_serializer.is_valid(raise_exception=True)
            return Response(error_serializer.data, status=error_serializer.data["code"])

        result = UpdateCommentOutputSerializer(instance=comment)

        return Response(result.data)
