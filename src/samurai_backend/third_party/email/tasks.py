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
) -> None:
    provider_builder().send_template_email(
        to=to,
        template_id=settings.email_registration_code_template_id,
        template_data={
            "code": code,
        },
    )


def send_reset_password_code_email(
    to: str,
    code: str,
) -> None:
    provider_builder().send_template_email(
        to=to,
        template_id=settings.email_reset_password_code_template_id,
        template_data={
            "code": code,
        },
    )


def send_notify_password_changed_email(
    to: str,
) -> None:
    provider_builder().send_template_email(
        to=to,
        template_id=settings.email_password_changed_template_id,
    )
