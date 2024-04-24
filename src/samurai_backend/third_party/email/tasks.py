from samurai_backend.settings import settings
from samurai_backend.third_party.email.providers.base import BaseEmailIntegration
from samurai_backend.third_party.email.providers.brevo import BrevoIntegration


def provider_builder() -> BaseEmailIntegration:
    if not settings.email_service_api_key:
        return BaseEmailIntegration(api_key="fake_api_key")

    return BrevoIntegration(
        api_key=settings.email_service_api_key,
    )


def send_registration_code_email(
    to: str,
    code: str,
    template_id: int = 1,
) -> None:
    provider_builder().send_template_email(
        to=to,
        template_id=template_id,
        template_data={
            "code": code,
        },
    )
