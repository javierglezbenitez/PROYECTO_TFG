import pandas as pd
from pathlib import Path

def export_clean_df(df: pd.DataFrame, output_path: str):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding='utf-8')
