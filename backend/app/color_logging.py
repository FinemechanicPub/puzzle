from copy import copy
from dataclasses import dataclass
import logging


@dataclass
class ColorCodes:
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    green = "\x1b[32;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"


LEVEL_COLOR = {
    logging.INFO: ColorCodes.green,
    logging.WARNING: ColorCodes.yellow,
    logging.ERROR: ColorCodes.red,
    logging.CRITICAL: ColorCodes.bold_red,
}


class ColorFormatter(logging.Formatter):
    def formatMessage(self, record: logging.LogRecord) -> str:
        record = copy(record)
        record.levelname = (
            LEVEL_COLOR[record.levelno]
            + record.levelname
            + ColorCodes.reset
            + ":"
            + f"{' ':<{9-len(record.levelname)}}"
        )
        return super().formatMessage(record)
