from rest_framework import serializers, status

from accounts.serializers.account.account_info import ShortTeacherInfoSerializer
from core.serializers.models import ModelWithUUID
from students.models import UserTask


class TaskSerializer(ModelWithUUID):
	reviewer = ShortTeacherInfoSerializer(allow_null=True)

	class Meta:
		model = UserTask
		fields = [
			"id",
			"order",
			"name",
			"description",
			"state",
			"reviewer",
			"due_date",
			"comments",  # Probably won't work, something has to be done for this
			"updated_at",
		]


class TaskNotFound(serializers.Serializer):
	error = serializers.CharField(default="TASK_NOT_FOUND")
	details = serializers.CharField(default="Task with specified task_id is not found")
	code = serializers.IntegerField(default=status.HTTP_404_NOT_FOUND)


class TaskFinderMixin:
	"""All serializers using this Mixin must have a property `student_entity`"""

	task: UserTask = None

	def validate_task_id(self, task_id):
		task_not_found = Exception(
			TaskNotFound(
				data={
					"details": f"Task not found with {task_id=}",
				}
			)
		)

		qs = UserTask.objects.filter(id=task_id)
		task = qs.first()
		if not task:
			raise task_not_found

		if not task.user_projects.filter(student=self.student_entity).exists():
			raise task_not_found

		self.task = task

		return task.id
