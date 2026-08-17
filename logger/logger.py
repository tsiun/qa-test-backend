import time
import logging
from logging.handlers import RotatingFileHandler
import os
import sys

from logger.logger_config import LoggerConfig


class Logger:
    __logger: logging.Logger | None = None

    @classmethod
    def _initialize_logger(cls) -> None:
        if cls.__logger is not None:
            return

        os.makedirs(LoggerConfig.LOGS_DIR_NAME, exist_ok=True)

        cls.__logger = logging.getLogger(LoggerConfig.LOGGER_NAME)
        cls.__logger.setLevel(LoggerConfig.LOGS_LEVEL)
        cls.__logger.propagate = False

        if cls.__logger.handlers:
            return

        formatter = logging.Formatter(
            LoggerConfig.FORMAT, datefmt=LoggerConfig.DATETIME_FORMAT
        )

        # UTC время
        formatter.converter = time.gmtime

        file_handler = RotatingFileHandler(
            LoggerConfig.LOGS_FILE_NAME,
            maxBytes=LoggerConfig.MAX_BYTES,
            backupCount=LoggerConfig.BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        cls.__logger.addHandler(file_handler)
        cls.__logger.addHandler(console_handler)

    @classmethod
    def _get_logger(cls) -> logging.Logger:
        cls._initialize_logger()
        return cls.__logger

    @classmethod
    def info(cls, message: str) -> None:
        cls._get_logger().info(msg=message)

    @classmethod
    def set_level(cls, level: str | int) -> None:
        cls._get_logger().setLevel(level)

    @classmethod
    def debug(cls, message: str) -> None:
        cls._get_logger().debug(msg=message)

    @classmethod
    def warning(cls, message: str) -> None:
        cls._get_logger().warning(msg=message)

    @classmethod
    def error(cls, message: str) -> None:
        cls._get_logger().error(msg=message)

    @classmethod
    def critical(cls, message: str) -> None:
        cls._get_logger().critical(msg=message)

    @classmethod
    def step(cls, message: str) -> None:
        cls._get_logger().info(msg=f"--- STEP: {message} ---")
