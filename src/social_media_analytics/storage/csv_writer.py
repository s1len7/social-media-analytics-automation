import json
from pathlib import Path
import pandas as pd

def normalize_data(data):
    rows = []
    for item in data:
        row = item.copy()
        if "raw_data" in row:
            row["raw_data"] = json.dumps(row["raw_data"], ensure_ascii=False)
        rows.append(row)
    return rows

def save_csv(data, filename):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe = pd.DataFrame(normalize_data(data))
    dataframe.to_csv(path, index=False, encoding="utf-8-sig")
    return path