from __future__ import annotations

import os
from typing import TYPE_CHECKING

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from drf_yasg import openapi
from rest_framework import serializers, status

from accounts.serializers.account.account_info import ShortTeacherInfoSerializer
from core.serializers.models import ModelWithUUID
from students.models.comment import Comment

if TYPE_CHECKING:
	from django.db.models.fields.files import FieldFile


class FileDetailsSerializer(serializers.Serializer):
	path_to_file = serializers.SerializerMethodField()
	file_size = serializers.SerializerMethodField()
	file_format = serializers.SerializerMethodField()

	def get_path_to_file(self, obj):
		if obj:
			return default_storage.url(obj.name)
		return None

	def get_file_size(self, obj) -> str:
		if obj:
			try:
				# Kilo, Mega, Giga
				K = 1_000
				M = K * K
				G = M * K
				bytes_size = default_storage.size(obj.name)
				prefix = "B"
				divider = 1
				if bytes_size >= G:
					divider = G
					prefix = "Impressive"
				elif bytes_size >= M:
					divider = M
					prefix = "MB"
				elif bytes_size >= K:
					divider = K
					prefix = "KB"
				return f"{round(bytes_size/divider, 2)}{prefix}"
			except (OSError, ObjectDoesNotExist):
				pass
		return "Unknown"

	def get_file_format(self, obj):
		if obj:
			_, file_extension = os.path.splitext(obj.name)
			return file_extension.lstrip(".").lower()
		return None


class FileRepresentationField(serializers.DictField):
	def to_representation(self, value: FieldFile | dict) -> FileDetailsSerializer | None:
		# When calling the second time (for some reason) - we get a dict
		if isinstance(value, dict):
			return value

		elif value.name:
			return FileDetailsSerializer(value).data
		return None

	class Meta:
		swagger_schema_fields = {
			"type": openapi.TYPE_OBJECT,
			"title": "File representation",
			"properties": {
				"path_to_file": openapi.Schema(
					title="(Relative) path to file",
					type=openapi.TYPE_STRING,
				),
				"file_size": openapi.Schema(
					title="Size of the file (with units)",
					type=openapi.TYPE_STRING,
				),
				"file_format": openapi.Schema(
					type=openapi.TYPE_STRING,
				),
			},
		}


class CommentSerializer(ModelWithUUID):
	author = ShortTeacherInfoSerializer()
	file = FileRepresentationField(allow_null=True)

	class Meta:
		model = Comment
		fields = "__all__"


class CommentNotFound(serializers.Serializer):
	error = serializers.CharField(default="COMMENT_NOT_FOUND")
	details = serializers.CharField(default="Comment with specified comment_id is not found")
	code = serializers.IntegerField(default=status.HTTP_404_NOT_FOUND)


class CommentFinderMixin:
	"""All serializers using this Mixin must have a property `student_entity`"""

	comment: Comment = None

	def validate_comment_id(self, comment_id):
		comment_not_found = Exception(
			CommentNotFound(
				data={
					"details": f"Comment not found with {comment_id=}",
				}
			)
		)

		qs = Comment.objects.all()
		qs = Comment.objects.filter(id=comment_id, author=self.student_entity)
		comment = qs.first()
		if not comment:
			raise comment_not_found

		self.comment = comment

		return comment.id
