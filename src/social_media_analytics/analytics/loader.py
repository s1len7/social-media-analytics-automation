import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_csv_files(data_path: Path) -> pd.DataFrame:
    dataframes = []

    for csv_file in data_path.glob("*.csv"):
        df = pd.read_csv(csv_file)
        logger.info(f"Loaded CSV: {csv_file.name}, rows={len(df)}")

        if "platform" in df.columns:
            platform_values = df["platform"].value_counts().to_dict()
            logger.info(f"Platform values: {csv_file.name}, {platform_values}")

        dataframes.append(df)

    if not dataframes:
        logger.warning(f"No CSV files found: {data_path}")
        return pd.DataFrame()

    df = pd.concat(
        dataframes,
        ignore_index=True,
        sort=False,
    )

    if "platform" in df.columns:
        platform_values = df["platform"].value_counts().to_dict()
        logger.info(f"Combined platform values: {platform_values}")

    return df


def normalize_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    timestamp = pd.Series(
        pd.NaT,
        index=df.index,
        dtype="datetime64[ns, UTC]",
    )

    instagram_mask = df["platform"] == "instagram"
    youtube_mask = df["platform"] == "youtube"

    if instagram_mask.any():
        timestamp.loc[instagram_mask] = pd.to_datetime(
            df.loc[instagram_mask, "timestamp"],
            utc=True,
            errors="coerce",
        )

    if youtube_mask.any():
        timestamp.loc[youtube_mask] = pd.to_datetime(
            df.loc[youtube_mask, "published_at"],
            utc=True,
            errors="coerce",
        )

    df["timestamp"] = timestamp

    parse_result = df.groupby("platform")["timestamp"].count().to_dict()

    logger.info(f"Timestamp parse result: {parse_result}")

    before_count = len(df)

    df = df.dropna(
        subset=["timestamp"],
    ).reset_index(drop=True)

    after_count = len(df)

    platform_result = df.groupby("platform").size().to_dict()

    logger.info(f"Timestamp normalized: before={before_count}, " f"after={after_count}, platform={platform_result}")

    return df
