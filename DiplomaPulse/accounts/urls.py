from django.urls import path

from . import views

autocomplete_urlpatterns = [
	path(
		route="autocomplete/base_user/",
		view=views.autocomplete.base_user.BaseUserAutocomplete.as_view(),
		name="base_user_autocomplete",
	),
	path(
		route="autocomplete/overseer/",
		view=views.autocomplete.overseer.OverseerAutocomplete.as_view(),
		name="overseer_autocomplete",
	),
	path(
		route="autocomplete/student/",
		view=views.autocomplete.student.StudentAutocomplete.as_view(),
		name="student_autocomplete",
	),
	path(
		route="autocomplete/teacher/",
		view=views.autocomplete.teacher.TeacherAutocomplete.as_view(),
		name="teacher_autocomplete",
	),
]

endpoint_urlpatterns = [
	path(
		route="token/",
		view=views.token.obtain_token_view.DecoratedTokenObtainPairView.as_view(),
		name="token_obtain_pair",
	),
	path(
		route="token/refresh/",
		view=views.token.refresh_token_view.DecoratedTokenRefreshView.as_view(),
		name="token_refresh",
	),
	path(
		route="sign-up/",
		view=views.account.sign_up.SignUpView.as_view(),
		name="sign_up",
	),
	path(
		route="account-info/",
		view=views.account.account_info.AccountInfoView.as_view(),
		name="account_info",
	),
]

urlpatterns = autocomplete_urlpatterns + endpoint_urlpatterns
