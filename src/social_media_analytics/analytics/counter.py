import pandas as pd


def yearly_count(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = dataframe.copy()

    dataframe["year"] = dataframe["timestamp"].dt.year.astype(int)

    result = (
        dataframe.groupby(
            ["year", "platform"],
        )
        .size()
        .reset_index(name="count")
    )

    result["year"] = result["year"].astype(int)
    result["count"] = result["count"].astype(int)

    return result


def monthly_count(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = dataframe.copy()

    dataframe["month"] = (
        dataframe["timestamp"].dt.tz_localize(None).dt.to_period("M").astype(str)
    )

    result = (
        dataframe.groupby(
            ["month", "platform"],
        )
        .size()
        .reset_index(name="count")
    )

    result["count"] = result["count"].astype(int)

    return result


def weekly_count(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = dataframe.copy()

    iso_calendar = dataframe["timestamp"].dt.tz_localize(None).dt.isocalendar()

    dataframe["week"] = (
        iso_calendar["year"].astype(str)
        + "_WW"
        + iso_calendar["week"].astype(str).str.zfill(2)
    )

    result = (
        dataframe.groupby(
            ["week", "platform"],
        )
        .size()
        .reset_index(name="count")
    )

    result["count"] = result["count"].astype(int)

    return result


def platform_count(dataframe: pd.DataFrame) -> pd.DataFrame:
    result = dataframe.groupby("platform").size().reset_index(name="count")

    result["count"] = result["count"].astype(int)

    return result
