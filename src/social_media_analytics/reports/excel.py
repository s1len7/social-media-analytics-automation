from pathlib import Path

import pandas as pd
from openpyxl.styles import Font, PatternFill


def auto_width(worksheet):
    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        worksheet.column_dimensions[column_letter].width = min(max_length + 2, 50)


def save_excel(summary, output_file):
    path = Path(output_file)

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for sheet_name, dataframe in summary.items():
            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]
            worksheet.freeze_panes = "A2"
            for cell in worksheet[1]:
                cell.font = Font(bold=True)
                cell.fill = PatternFill("solid", fgColor="D9D9D9")
            auto_width(worksheet)

    return path
