"""This module creates a logger object for the samurai_backend package."""

import logging

from samurai_backend.settings import settings

main_logger = logging.getLogger("samurai_backend")

main_logger.setLevel(settings.logging_level)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)
handler.setFormatter(formatter)

main_logger.addHandler(handler)
