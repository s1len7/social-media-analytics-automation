import pandas as pd

from social_media_analytics.analytics.counter import (
    monthly_count,
    platform_count,
    weekly_count,
    yearly_count,
)


def create_summary(dataframe: pd.DataFrame) -> dict:
    summary = {
        "platform": platform_count(dataframe),
        "yearly": yearly_count(dataframe),
        "monthly": monthly_count(dataframe),
        "weekly": weekly_count(dataframe),
    }

    return summary