import logging
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)


def create_bar_chart(
    dataframe,
    x_column,
    output_path: Path,
):
    plt.figure(figsize=(12, 6))

    sns.barplot(
        data=dataframe,
        x=x_column,
        y="count",
        hue="platform",
    )

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()


def save_yearly_chart(
    dataframe,
    output_path: Path,
):
    create_bar_chart(
        dataframe,
        "year",
        output_path,
    )


def save_monthly_chart(
    dataframe,
    output_path: Path,
):
    create_bar_chart(
        dataframe,
        "month",
        output_path,
    )


def save_weekly_chart(
    dataframe,
    output_path: Path,
):
    create_bar_chart(
        dataframe,
        "week",
        output_path,
    )