import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_csv_files(data_path: Path) -> pd.DataFrame:
    dataframes = []

    for csv_file in data_path.glob("*.csv"):
        dataframe = pd.read_csv(csv_file)

        logger.info(
            f"Loaded CSV: {csv_file.name}, rows={len(dataframe)}"
        )

        if "platform" in dataframe.columns:
            logger.info(
                f"Platform values: {csv_file.name}, "
                f"{dataframe['platform'].value_counts().to_dict()}"
            )

        dataframes.append(dataframe)

    dataframe = pd.concat(
        dataframes,
        ignore_index=True,
        sort=False,
    )

    logger.info(
        f"Combined platform values: "
        f"{dataframe['platform'].value_counts().to_dict()}"
    )

    return dataframe


def normalize_timestamp(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = dataframe.copy()

    timestamp = pd.Series(
        pd.NaT,
        index=dataframe.index,
        dtype="datetime64[ns, UTC]",
    )

    instagram_mask = dataframe["platform"] == "instagram"
    youtube_mask = dataframe["platform"] == "youtube"

    if instagram_mask.any():
        timestamp.loc[instagram_mask] = pd.to_datetime(
            dataframe.loc[
                instagram_mask,
                "timestamp",
            ],
            utc=True,
            errors="coerce",
        )

    if youtube_mask.any():
        timestamp.loc[youtube_mask] = pd.to_datetime(
            dataframe.loc[
                youtube_mask,
                "published_at",
            ],
            utc=True,
            errors="coerce",
        )

    dataframe["timestamp"] = timestamp

    parse_result = (
        dataframe.groupby("platform")["timestamp"]
        .count()
        .to_dict()
    )

    logger.info(
        f"Timestamp parse result: {parse_result}"
    )

    before = len(dataframe)

    dataframe = dataframe.dropna(
        subset=["timestamp"],
    ).reset_index(drop=True)

    after = len(dataframe)

    platform_result = (
        dataframe.groupby("platform")
        .size()
        .to_dict()
    )

    logger.info(
        f"Timestamp normalized: "
        f"before={before}, after={after}, "
        f"platform={platform_result}"
    )

    return dataframe