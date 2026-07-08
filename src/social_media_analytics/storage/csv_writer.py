from pathlib import Path
import pandas as pd


def save_csv(data, filename):

    path = Path(filename)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    dataframe = pd.DataFrame(data)

    dataframe.to_csv(
        path,
        index=False,
        encoding="utf-8-sig"
    )

    return path