from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework_simplejwt.views import TokenObtainPairView


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):  # noqa
        raise NotImplementedError()

    def update(self, instance, validated_data):  # noqa
        raise NotImplementedError()


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        },
        tags=["token"],
    )
    def post(self, request, *args, **kwargs):  # noqa
        return super().post(request, *args, **kwargs)
