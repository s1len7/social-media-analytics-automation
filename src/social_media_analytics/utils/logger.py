import logging
from pathlib import Path


def setup_logger(level, log_file):
    logger = logging.getLogger()
    logger.setLevel(
        getattr(
            logging,
            level.upper(),
            logging.INFO,
        )
    )

    for handler in logger.handlers:
        logger.removeHandler(handler)

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        formatter,
    )

    logger.addHandler(
        console_handler,
    )

    log_path = Path(log_file)
    log_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_handler = logging.FileHandler(
        log_path,
        encoding="utf-8",
    )

    file_handler.setFormatter(
        formatter,
    )

    logger.addHandler(
        file_handler,
    )

    logger.info(f"Log file initialized: {log_path}")

    return logger
