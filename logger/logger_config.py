import logging
from pathlib import Path


class LoggerConfig:
    LOGS_DIR_NAME = Path("logs")
    LOGGER_NAME = "Logger"
    LOGS_FILE_NAME = LOGS_DIR_NAME / "api.log"

    LOGS_LEVEL = logging.INFO

    MAX_BYTES = 100000
    BACKUP_COUNT = 3

    # FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    FORMAT = "%(asctime)s.%(msecs)03d | %(module)10s:%(lineno)-3d | %(levelname)-7s | %(message)s"
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
