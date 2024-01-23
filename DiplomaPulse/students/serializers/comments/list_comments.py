from django.core.paginator import Paginator
from rest_framework import serializers

from students.serializers.base import AccountSerializerMixIn
from students.serializers.tasks.task import TaskFinderMixin

from .comment import CommentSerializer


class ListCommentsInputSerializer(serializers.Serializer):
	task_id = serializers.UUIDField()
	page = serializers.IntegerField(default=1)
	page_size = serializers.IntegerField(default=25)


class ListCommentsOutputSerializer(serializers.Serializer):
	pages = serializers.IntegerField(min_value=1, default=1)
	data = CommentSerializer(many=True)


class ListCommentsSerializer(TaskFinderMixin, AccountSerializerMixIn, ListCommentsInputSerializer):
	output_serializer: ListCommentsOutputSerializer = None

	def validate(self, attrs):
		attrs = super().validate(attrs)

		page = attrs["page"]
		page_size = attrs["page_size"]

		paginator = Paginator(
			object_list=self.task.comments.all(),
			per_page=page_size,
		)

		comments_list = paginator.get_page(page)
		total_pages = paginator.num_pages

		comments = CommentSerializer(instance=comments_list, many=True)

		self.output_serializer = ListCommentsOutputSerializer(
			data={
				"pages": total_pages,
				"data": comments.data,
			}
		)

		self.output_serializer.is_valid(raise_exception=True)

		return attrs

	def create(self):
		return self.output_serializer
