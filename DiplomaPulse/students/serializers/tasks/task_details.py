from rest_framework import serializers, status

from students.models.task import UserTask
from students.serializers.base import AccountSerializerMixIn
from students.serializers.tasks.task import TaskSerializer


class TaskDetailsInputSerializer(serializers.Serializer):
	task_id = serializers.UUIDField()


class TaskDetailsOutputSerializer(TaskSerializer):
	pass


class GetTaskDetailsSerializer(AccountSerializerMixIn, TaskDetailsInputSerializer):
	task: UserTask = None

	def validate_task_id(self, task_id):
		task_not_found = serializers.ValidationError(
			detail=f"Task not found with {task_id=}",
			code=status.HTTP_404_NOT_FOUND,
		)

		qs = UserTask.objects.filter(id=task_id)
		task = qs.first()
		if not task:
			raise task_not_found

		if not task.user_projects.filter(student=self.student_entity).exists():
			raise task_not_found

		self.task = task

		return task.id

	def create(self):
		return TaskDetailsOutputSerializer(self.task)
