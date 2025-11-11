import pandas as pd
import numpy as np


def find_candidate_blocks(excel_path, min_cols=3):
    df = pd.read_excel(excel_path, header=None, dtype=str)
    df = df.replace(r'^\s*$', np.nan, regex=True)
    non_empty_counts = df.notna().sum(axis=1)

    threshold = max(non_empty_counts.max() * 0.5, min_cols)
    candidate_rows = non_empty_counts[non_empty_counts >= threshold].index.tolist()
    if not candidate_rows:
        return []

    blocks, start = [], None
    for i in range(len(candidate_rows)):
        if start is None:
            start = candidate_rows[i]
        if i == len(candidate_rows) - 1 or candidate_rows[i + 1] - candidate_rows[i] > 3:
            end = candidate_rows[i]
            blocks.append((start, end))
            start = None

    tables = []
    for start, end in blocks:
        sub_df = df.loc[start:end].dropna(how="all", axis=1)
        tables.append({"start": start, "end": end, "data": sub_df.to_json()})
    
    return tables