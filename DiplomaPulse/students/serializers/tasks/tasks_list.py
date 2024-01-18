from django.core.paginator import Paginator
from rest_framework import serializers, status

from students.models.project import UserProject
from students.models.task import UserTask
from students.serializers.base import AccountSerializerMixIn
from students.serializers.tasks.task import TaskSerializer


class TaskListInputSerializer(serializers.Serializer):
	project_id = serializers.UUIDField(required=False, allow_null=True)
	page = serializers.IntegerField(default=1, min_value=1)
	page_size = serializers.IntegerField(default=25, min_value=1)


class TasksListOutputSerializer(serializers.Serializer):
	pages = serializers.IntegerField(min_value=1)
	data = TaskSerializer(many=True)


class GetTasksListSerializer(AccountSerializerMixIn, TaskListInputSerializer):
	project_entity: UserProject = None
	tasks_list: list[UserTask] = None
	total_pages: int = None

	def validate_project_id(self, project_id):
		projects_qs = UserProject.objects.order_by("updated_at").filter(student=self.student_entity)
		if project_id:
			projects_qs = projects_qs.filter(id=project_id)

		project_entity = projects_qs.first()
		if not project_entity:
			raise serializers.ValidationError(
				detail=f"Project not found with {project_id=}",
				code=status.HTTP_404_NOT_FOUND,
			)

		self.project_entity = project_entity
		return project_entity.id

	def validate(self, attrs: dict):
		attrs = super().validate(attrs)

		page = attrs["page"]
		page_size = attrs["page_size"]

		paginator = Paginator(self.project_entity.tasks.all(), per_page=page_size)

		self.tasks_list = paginator.get_page(page)
		self.total_pages = paginator.num_pages

		return attrs

	def create(self):
		tasks_serializer = TaskSerializer(
			instance=self.tasks_list,
			many=True,
		)
		return TasksListOutputSerializer(
			data={
				"pages": self.total_pages,
				"data": tasks_serializer.data,
			}
		)
