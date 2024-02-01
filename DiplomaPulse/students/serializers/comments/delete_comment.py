from django.db.transaction import atomic
from rest_framework import serializers

from students.serializers.base import AccountSerializerMixIn

from .comment import CommentFinderMixin


class DeleteCommentInputSerializer(serializers.Serializer):
	comment_id = serializers.UUIDField()


class DeleteCommentOutputSerializer(serializers.Serializer):
	removed = serializers.BooleanField(default=False)


class DeleteCommentSerializer(
	AccountSerializerMixIn,
	CommentFinderMixin,
	DeleteCommentInputSerializer,
):
	@atomic
	def delete(self):
		self.comment.delete()

		serializer = DeleteCommentOutputSerializer(data={"removed": True})
		serializer.is_valid(raise_exception=True)
		return serializer
