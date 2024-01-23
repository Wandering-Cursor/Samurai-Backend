from django.http import HttpResponseRedirect
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from DiplomaPulse.logger import main_logger


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
		main_logger.info("Attempt of accessing the main page")
		return HttpResponseRedirect("/swagger/")
