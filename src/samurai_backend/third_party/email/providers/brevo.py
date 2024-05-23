from urllib.parse import urljoin

from samurai_backend.log import events_logger
from samurai_backend.third_party.email.providers.base import BaseEmailIntegration
from samurai_backend.third_party.requests.sender import RequestSender


class BrevoIntegration(BaseEmailIntegration):
    def __init__(
        self: "BrevoIntegration",
        api_key: str,
    ) -> None:
        super().__init__(api_key)

        self.sender = RequestSender()
        self.test_mode = False

    def use_test_mode(self: "BrevoIntegration") -> None:
        self.test_mode = True

    def use_production_mode(self: "BrevoIntegration") -> None:
        self.test_mode = False

    @property
    def base_api_url(self: "BrevoIntegration") -> str:
        return "https://api.brevo.com"

    @property
    def headers(self: "BrevoIntegration") -> dict[str, str]:
        return {
            "api-key": self.api_key,
            "Content-Type": "application/json",
        }

    def make_url(self: "BrevoIntegration", endpoint: str) -> str:
        return urljoin(self.base_api_url, endpoint)

    def send_template_email(
        self: "BrevoIntegration",
        to: list[str] | str,
        template_id: int,
        template_data: dict[str, str] | None,
    ) -> None:
        if isinstance(to, str):
            to = [
                {
                    "name": to,
                    "email": to,
                }
            ]
        elif isinstance(to, list):
            to = [
                {
                    "name": name,
                    "email": email,
                }
                for name, email in zip(to, to, strict=True)
            ]

        json_data = {
            "to": to,
            "templateId": template_id,
        }
        if template_data:
            json_data["templateData"] = template_data

        if self.test_mode:
            json_data["X-Sib-Sandbox"] = "drop"

        response = self.sender.send_request(
            "POST",
            self.make_url("/v3/smtp/email"),
            json=json_data,
            headers=self.headers,
        )
        try:
            value = self.sender.get_json(response)
        except ValueError:
            events_logger.exception(
                f"Error parsing Brevo response: {response.text} ({response.status_code})"
            )
            raise

        events_logger.debug(f"Brevo response: {value=}")
