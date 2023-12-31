from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt import authentication

from .views import MainPageView

schema_view = get_schema_view(
	openapi.Info(
		title="Samurai API",
		default_version="v1",
		description="API Definition for Samurai project",
		terms_of_service="",
		contact=openapi.Contact(email="hdydpavel@gmail.com"),
		license=openapi.License(name="MIT License"),
	),
	public=True,
	authentication_classes=(authentication.JWTAuthentication,),
	permission_classes=(permissions.AllowAny,),
	url=settings.BASE_URL,
)

static_patterns = static(
	settings.STATIC_URL,
	document_root=settings.STATIC_ROOT,
)
media_patterns = static(
	settings.MEDIA_URL,
	document_root=settings.MEDIA_ROOT,
)

django_patterns = (
	[
		path("admin/", admin.site.urls),
	]
	+ static_patterns
	+ media_patterns
)

swagger_patterns = [
	path(
		"swagger<format>/",
		schema_view.without_ui(cache_timeout=0),
		name="schema-json",
	),
	path(
		"swagger/",
		schema_view.with_ui("swagger", cache_timeout=0),
		name="schema-swagger-ui",
	),
]

custom_patterns = [
	path("", MainPageView.as_view()),
	path("api/accounts/", include("accounts.urls")),
	path("api/students/", include("students.urls")),
]

urlpatterns = django_patterns + swagger_patterns + custom_patterns
