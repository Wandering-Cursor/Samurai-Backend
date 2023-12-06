from rest_framework.views import APIView
from rest_framework.response import Response


class BaseApiView(APIView):
    pass


class AuthenticatedApiView(BaseApiView):
    pass


class PublicApiView(BaseApiView):
    pass


class MainPageView(PublicApiView):
    def get(self, request):
        return Response("Hello, world!!!")
