from rest_framework import serializers

from students.serializers.base import AccountSerializerMixIn
from students.serializers.tasks.task import TaskFinderMixin, TaskSerializer


class TaskDetailsInputSerializer(serializers.Serializer):
	task_id = serializers.UUIDField()


class TaskDetailsOutputSerializer(TaskSerializer):
	pass


class GetTaskDetailsSerializer(AccountSerializerMixIn, TaskDetailsInputSerializer, TaskFinderMixin):
	def create(self):
		return TaskDetailsOutputSerializer(self.task)
