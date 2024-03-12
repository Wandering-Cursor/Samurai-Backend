from rest_framework import serializers


class ModelWithUUID(serializers.ModelSerializer):
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
