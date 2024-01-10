from rest_framework import serializers


class ModelWithUUID(serializers.ModelSerializer):
	id = serializers.UUIDField()
