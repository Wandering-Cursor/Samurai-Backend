from django.urls import path

from . import views

project_patterns = [
	path(
		"project",
		views.project.last_project.GetLastProjectView.as_view(),
		name="get_last_project",
	),
]

tasks_patterns = [
	path(
		"tasks/overview",
		views.tasks.tasks_overview.GetTasksOverview.as_view(),
		name="get_tasks_overview",
	),
	path(
		"tasks/list",
		views.tasks.tasks_list.GetTasksList.as_view(),
		name="get_tasks_list",
	),
	path(
		"tasks/task",
		views.tasks.task_details.GetTaskDetails.as_view(),
		name="get_task_details",
	),
	path(
		"tasks/move_task",
		views.tasks.task_update.UpdateTask.as_view(),
		name="update_task_state",
	),
]

comments_patterns = [
	path(
		"comments/add",
		views.comments.new_comment.AddCommentView.as_view(),
		name="add_comment",
	)
]

urlpatterns = project_patterns + tasks_patterns + comments_patterns
