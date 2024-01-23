from .settings import *  # noqa
from .settings import LOGGING

# Uncomment if you need more logs
for logger in LOGGING["loggers"].keys():
	LOGGING["loggers"][logger]["handlers"] += ["console"]
# 	LOGGING["loggers"][logger]["level"] = "DEBUG"

# for handler in LOGGING["handlers"].keys():
# 	LOGGING["handlers"][handler]["level"] = "DEBUG"
# LOGGING["root"]["level"] = "DEBUG"
