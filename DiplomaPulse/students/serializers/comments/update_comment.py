from django.core.files.base import ContentFile
from django.db.transaction import atomic
from django.utils.crypto import get_random_string
from rest_framework import serializers

from core.serializers.fields import Base64Field
from students.models.comment import Comment
from students.serializers.base import AccountSerializerMixIn
from students.serializers.comments.comment import CommentFinderMixin, validate_comment_content

from .comment import CommentSerializer


class UpdateCommentInputSerializer(serializers.Serializer):
	comment_id = serializers.UUIDField()
	file_name = serializers.CharField(
		required=False,
		allow_null=True,
	)
	file_content = Base64Field(
		required=False,
		allow_null=True,
	)
	text = serializers.CharField(
		required=False,
		allow_blank=False,
		allow_null=True,
		trim_whitespace=False,  # I believe it's cool :)
	)


class UpdateCommentOutputSerializer(CommentSerializer):
	pass


class UpdateCommentSerializer(
	AccountSerializerMixIn, UpdateCommentInputSerializer, CommentFinderMixin
):
	def validate(self, attrs):
		attrs = super().validate(attrs)

		attrs = validate_comment_content(attrs)

		return attrs

	def update(self, instance: Comment, validated_data: dict) -> Comment:
		with atomic():
			file = None
			if file_content := validated_data.get("file_content", None):
				file_name = validated_data.get("file_name")
				file_name = f"{get_random_string(length=12)}_{file_name}"

				file = ContentFile(
					content=file_content,
					name=file_name,
				)

			instance.file = file
			instance.text = validated_data.get("text", None)
			instance.save()

			return instance
