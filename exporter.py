import pandas as pd

def export_to_excel(df: pd.DataFrame, filepath: str) -> None:
    """Export DataFrame to Excel."""
    df.to_excel(filepath, index=False)

def export_to_csv(df: pd.DataFrame, filepath: str) -> None:
    """Export DataFrame to CSV."""
    df.to_csv(filepath, index=False)