from rest_framework import serializers, status

from students.choices import TaskState
from students.models.project import UserProject
from students.serializers.base import AccountSerializerMixIn
from students.serializers.tasks.task import TaskSerializer


class TasksOverviewStatisticsByStatus(serializers.Serializer):
	new = serializers.IntegerField(min_value=0)
	in_progress = serializers.IntegerField(min_value=0)
	in_review = serializers.IntegerField(min_value=0)
	reopened = serializers.IntegerField(min_value=0)
	done = serializers.IntegerField(min_value=0)


class TaskOverviewStatistics(serializers.Serializer):
	total = serializers.IntegerField(min_value=0)
	by_status = TasksOverviewStatisticsByStatus()


class TasksOverviewSerializer(serializers.Serializer):
	statistics = TaskOverviewStatistics()


class TasksOverviewInputSerializer(serializers.Serializer):
	project_id = serializers.UUIDField(default=None, required=False, allow_null=True)


class TasksOverviewOutputSerializer(serializers.Serializer):
	statistics = TasksOverviewSerializer()
	recent = TaskSerializer(many=True)


class GetTasksOverviewSerializer(AccountSerializerMixIn, TasksOverviewInputSerializer):
	project_entity: UserProject = None

	def validate(self, attrs):
		attrs = super().validate(attrs)

		student = self.student_entity
		project_id = attrs.get("project_id")

		project_qs = None

		if project_id:
			project_qs = UserProject.objects.filter(student=student, id=project_id)

		else:
			project_qs = UserProject.objects.filter(student=student).order_by("created_at")

		if not project_qs.exists():
			raise serializers.ValidationError(
				detail={"project_id": "Could not find a project with specified ID"},
				code=status.HTTP_404_NOT_FOUND,
			)
		self.project_entity = project_qs.first()
		if not self.project_entity:
			raise ValueError("QS exists, but entity is None!")

		return attrs

	def create(self) -> tuple[TasksOverviewSerializer, TaskSerializer]:
		project = self.project_entity

		by_status_statistics = TasksOverviewStatisticsByStatus(
			data={
				"new": project.tasks.filter(state=TaskState.NEW).count(),
				"in_progress": project.tasks.filter(state=TaskState.IN_PROGRESS).count(),
				"in_review": project.tasks.filter(state=TaskState.IN_REVIEW).count(),
				"reopened": project.tasks.filter(state=TaskState.REOPENED).count(),
				"done": project.tasks.filter(state=TaskState.DONE).count(),
			}
		)
		by_status_statistics.is_valid(raise_exception=True)

		statistics = TaskOverviewStatistics(
			data={
				"total": project.tasks.count(),
				"by_status": by_status_statistics.data,
			}
		)
		statistics.is_valid(raise_exception=True)

		return TasksOverviewSerializer(
			data={
				"statistics": statistics.data,
			},
		), TaskSerializer(project.tasks.order_by("created_at")[:5], many=True)
