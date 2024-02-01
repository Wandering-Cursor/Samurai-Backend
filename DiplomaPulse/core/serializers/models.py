from rest_framework import serializers


class ModelWithUUID(serializers.ModelSerializer):
	id = serializers.UUIDField()
	created_at = serializers.DateTimeField()
	updated_at = serializers.DateTimeField()
