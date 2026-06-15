import pandas as pd


def normalize_names(df: pd.DataFrame) -> pd.DataFrame:
    df["University"] = df["University"].str.strip().str.lower()
    df = df.drop_duplicates(subset="University")
    return df