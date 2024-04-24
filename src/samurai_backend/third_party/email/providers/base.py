from samurai_backend.log import events_logger


class BaseEmailIntegration:
    def __init__(
        self: "BaseEmailIntegration",
        api_key: str,
    ) -> None:
        self.api_key = api_key

    @property
    def base_api_url(self: "BaseEmailIntegration") -> str:
        raise NotImplementedError("You must implement this property")

    def send_template_email(
        self: "BaseEmailIntegration",
        to: list[str] | str,
        template_id: int,
        template_data: dict[str, str],
    ) -> None:
        events_logger.debug(f"Sending email to {to=}, {template_id=}, {template_data=}")
