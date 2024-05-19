"""This module creates a logger object for the samurai_backend package."""

import logging

from samurai_backend.settings import settings

main_logger = logging.getLogger("samurai_backend")
events_logger = logging.getLogger("samurai_backend_events")

main_logger.setLevel(settings.logging_level)
events_logger.setLevel(settings.events_logging_level)


def handler_factory() -> logging.Handler:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    handler.setFormatter(formatter)
    return handler


for logger in logging.Logger.manager.loggerDict.values():
    if isinstance(logger, logging.Logger):
        if logger.name.startswith("uvicorn."):
            logger.handlers.clear()

        logger.addHandler(handler_factory())
