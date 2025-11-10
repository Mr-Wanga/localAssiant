import os
import sys
import json
import queue
import logging
import threading
from datetime import datetime
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "time": datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)
        return json.dumps(log, ensure_ascii=False)

def _ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def get_logger(
    name: str = "mcp",
    log_dir: str = "./logs",
    level: str = "INFO",
    json_mode: bool = True,
    rotate: str = "size",
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 5,
    async_mode: bool = True
) -> logging.Logger:
    """
    Args:
        name (str): logging name
        log_dir (str): logging directory
        level (str): logging level
        json_mode (bool): If use json format
        rotate (str): "size" or "daily"
        max_bytes (int): One file max size
        backup_count (int): Max file count
        async_mode (bool): If support async write

    Returns:
        logging.Logger
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"{name}_{date_str}.log")
    _ensure_dir(log_file)

    formatter = JsonFormatter() if json_mode else logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    if rotate == "daily":
        handler = logging.FileHandler(log_file, encoding="utf-8")
    else:
        handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )

    handler.setFormatter(formatter)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)

    if async_mode:
        log_queue = queue.Queue(-1)
        queue_handler = QueueHandler(log_queue)
        listener = QueueListener(log_queue, handler, console, respect_handler_level=True)
        listener_thread = threading.Thread(target=listener.start, daemon=True)
        listener_thread.start()

        logger.addHandler(queue_handler)
        logger._queue_listener = listener
    else:
        logger.addHandler(handler)
        logger.addHandler(console)

    return logger
