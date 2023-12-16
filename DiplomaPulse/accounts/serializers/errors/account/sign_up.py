from rest_framework import serializers, exceptions


class RegistrationCodeNotFound(exceptions.NotFound):
    default_detail = "Invalid registration code"
    default_code = "registration_code_not_found"
    status_code = 404

    help_text = "Description of the error with the registration code"


class SignUpErrorSerializer(serializers.Serializer):
    registration_code = serializers.CharField(
        help_text=RegistrationCodeNotFound.help_text,
        default=RegistrationCodeNotFound.default_detail,
    )
