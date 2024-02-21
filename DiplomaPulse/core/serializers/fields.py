import base64
import binascii

from rest_framework import serializers

from DiplomaPulse.logger import main_logger


class Base64Field(serializers.Field):
    def to_internal_value(self, data: str) -> bytes:
        try:
            return base64.b64decode(data)
        except (TypeError, binascii.Error) as e:
            main_logger.error(f"Invalid Base64 data: {data=}\nError: {e=}")
            raise serializers.ValidationError("Invalid Base64 data") from e

    def to_representation(self, value: bytes) -> str:
        return base64.b64encode(value).decode("utf-8")
