import datetime

from samurai_backend.settings import settings


def current_time() -> datetime.datetime:
    return datetime.datetime.now(tz=settings.timezone)
