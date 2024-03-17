import json
import logging
from datetime import datetime

import uvicorn.logging


class JSONFormatter(logging.Formatter):
    def format(self, record) -> str:
        log_data = {
            "level": record.levelname,
            "message": None,
            "context": record.name,
            "timestamp": datetime.utcnow().timestamp(),
        }

        if record.name == "uvicorn.access":
            (
                log_data["remote"],
                log_data["method"],
                log_data["endpoint"],
                log_data["http_version"],
                log_data["status_code"],
            ) = record.args
            log_data["message"] = "%s - %s %s" % (
                log_data["status_code"],
                log_data["method"],
                log_data["endpoint"],
            )
        else:
            log_data["message"] = record.getMessage()

        if record.exc_info:
            log_data["exc_info"] = record.exc_info

        return json.dumps(log_data)


def setup_logging(config):
    log_level_name = config.get("log_level", "info")
    is_debug_mode = config.get("debug", False, type=bool)

    log_level = getattr(logging, log_level_name.upper())

    if is_debug_mode:
        log_formatter = uvicorn.logging.ColourizedFormatter("%(levelprefix)s %(message)s", style="%", use_colors=True)
    else:
        log_formatter = JSONFormatter()

    logger = logging.getLogger("shopping")
    logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(log_formatter)
    logger.addHandler(handler)

    logger = logging.getLogger("uvicorn")
    logger.handlers[0].setLevel(log_level)
    logger.handlers[0].setFormatter(log_formatter)

    logger = logging.getLogger("uvicorn.access")
    logger.handlers[0].setLevel(log_level)
    logger.handlers[0].setFormatter(log_formatter)
