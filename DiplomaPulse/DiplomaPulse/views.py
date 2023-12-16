from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseApiView(APIView):
	# For now, there are no additional checks for all views
	pass


class AuthenticatedApiView(BaseApiView):
	# This view should be used for all authenticated endpoints
	permission_classes = [IsAuthenticated]


class PublicApiView(BaseApiView):
	# This view should be used for all public endpoints
	permission_classes = [AllowAny]


class MainPageView(PublicApiView):
	def get(self, request):
		return Response({"text": "Hello, world!"})
