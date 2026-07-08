from pathlib import Path

import pandas as pd


def save_csv(data, output_file):
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)

    dataframe = pd.DataFrame(data)

    if "platform" not in dataframe.columns:
        raise ValueError("Missing platform column")

    dataframe["platform"] = dataframe["platform"].fillna("").str.lower().str.strip()

    dataframe.to_csv(path, index=False, encoding="utf-8-sig")

    return len(dataframe)
