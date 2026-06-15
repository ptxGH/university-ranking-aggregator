import pandas as pd

def load_the_from_csv(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df = df[["University", "Score"]]
    df.columns = ["University", "THE"]
    return df