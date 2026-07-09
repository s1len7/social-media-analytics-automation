import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


def get_report_month():
    today = datetime.today()

    if today.month == 1:
        return f"{today.year - 1}-12"

    return f"{today.year}-{today.month - 1:02d}"


def should_run(state_file: Path) -> bool:
    report_month = get_report_month()

    if not state_file.exists():
        logger.info("State file not found. Run analytics.")
        return True

    try:
        state = json.loads(
            state_file.read_text(
                encoding="utf-8",
            )
        )
    except Exception as error:
        logger.warning(f"Invalid state file: {error}")
        return True

    last_report_month = state.get(
        "last_report_month",
    )

    if last_report_month == report_month:
        logger.info(f"Report already sent: {report_month}")
        return False

    logger.info(f"New report required: {report_month}")
    return True


def save_state(state_file: Path):
    state_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    state = {
        "last_run_time": datetime.now().isoformat(
            timespec="seconds",
        ),
        "last_report_month": get_report_month(),
    }

    state_file.write_text(
        json.dumps(
            state,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    logger.info(f"State saved: {state_file}")
