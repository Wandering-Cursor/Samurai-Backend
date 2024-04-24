import uuid
from typing import Literal

import httpx
from pydantic.types import JsonValue

from samurai_backend.log import events_logger
from samurai_backend.settings import settings


class RequestSender:
    def __init__(
        self: "RequestSender",
        default_timeout: int = 10,
    ) -> None:
        self.default_headers = {
            "User-Agent": f"Samurai-Backend/{settings.app_version}",
            "X-Request-Id": uuid.uuid4().hex,
        }
        self.default_timeout = default_timeout

    def send_request(  # noqa:PLR0913
        self: "RequestSender",
        method: Literal["GET", "POST", "PUT", "DELETE"],
        url: str,
        headers: dict[str, str] | None = None,
        data: dict[str, str] | None = None,
        json: dict[str, str] | None = None,
        query: dict[str, str] | None = None,
        timeout: int | None = None,
    ) -> httpx.Response:
        try:
            events_logger.debug(f"Sending request ({method=}) to {url=}")
            events_logger.debug(f"{data=} - {json=} - {query=}")
            return httpx.request(
                method=method,
                url=url,
                params=query,
                data=data,
                json=json,
                timeout=self.default_timeout or timeout,
                headers={**self.default_headers, **(headers or {})},
            )
        except httpx.HTTPError as e:
            events_logger.error(f"Error sending request to {url=}")

            raise e

    @staticmethod
    def get_json(response: httpx.Response) -> JsonValue:
        """Be aware - this method will raise an exception if the response is not JSON."""
        return response.json()
