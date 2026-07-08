import json
from datetime import datetime
from pathlib import Path


def get_report_month():
    today = datetime.today()

    if today.month == 1:
        return f"{today.year - 1}-12"

    return f"{today.year}-{today.month - 1:02d}"


def should_run(state_file):
    report_month = get_report_month()

    if not state_file.exists():
        return True

    state = json.loads(
        state_file.read_text(
            encoding="utf-8",
        )
    )

    return (
        state.get("last_report_month")
        != report_month
    )


def save_state(state_file):
    state_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    state = {
        "last_run_time": datetime.now().isoformat(timespec="seconds",),
        "last_report_month": get_report_month(),
    }

    state_file.write_text(json.dumps(state, indent=4,), encoding="utf-8",)