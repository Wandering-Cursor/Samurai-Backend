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
	)
]

urlpatterns = project_patterns + tasks_patterns
