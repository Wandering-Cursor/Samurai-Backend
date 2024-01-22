from django.db.models import TextChoices
from django.db.transaction import atomic
from django.utils.crypto import get_random_string
from rest_framework import serializers

from core.serializers.fields import Base64Field
from DiplomaPulse.logger import main_logger
from students.models.comment import Comment
from students.serializers.base import AccountSerializerMixIn
from students.serializers.tasks.task import TaskFinderMixin

from .comment import CommentSerializer


class BadCommentErrorCodes(TextChoices):
	INVALID_FILE = "INVALID_FILE", "INVALID_FILE"
	INVALID_ARGUMENTS = "INVALID_ARGUMENTS", "INVALID_ARGUMENTS"


class BadCommentRequest(serializers.Serializer):
	error = serializers.ChoiceField(BadCommentErrorCodes.choices)
	code = serializers.IntegerField(default=400)


class NewCommentInputSerializer(serializers.Serializer):
	task_id = serializers.UUIDField()
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


class NewCommentOutputSerializer(CommentSerializer):
	pass


class AddCommentSerializer(AccountSerializerMixIn, NewCommentInputSerializer, TaskFinderMixin):
	def validate(self, args: dict):
		args: dict = super().validate(args)

		comment_text = args.get("text", None)
		file_name, file_content = args.get("file_name"), args.get("file_content")

		if comment_text and any([file_name, file_content]):
			main_logger.error("Got comment_text and file parameters")
			raise Exception(
				BadCommentRequest(
					data={
						"error": BadCommentErrorCodes.INVALID_ARGUMENTS,
					}
				)
			)

		if any([file_name, file_content]) and not all([file_name, file_content]):
			main_logger.error(
				f"Got one of file_arguments, but not both: {str(file_name)[:100]=}"
				f"{str(file_content)[:100]=}"
			)
			raise Exception(
				BadCommentRequest(
					data={
						"error_code": BadCommentErrorCodes.INVALID_ARGUMENTS,
					}
				)
			)

		return args

	def create(self, validated_data) -> Comment:
		with atomic():
			from django.core.files.base import ContentFile

			comment = Comment.objects.create(
				file=ContentFile(
					content=validated_data.get("file_content", None),
					name=f"{get_random_string(length=12)}_{validated_data.get('file_name', None)}",
				),
				text=validated_data.get("text", None),
				author=self.student_entity,
			)

			return comment
