import pandas as pd

def calculate_aggregate(df: pd.DataFrame,
                        w_qs: float,
                        w_the: float,
                        w_arwu: float) -> pd.DataFrame:
    df = df.fillna(0)

    df["Final Score"] = (
            df["QS"] * w_qs +
            df["THE"] * w_the +
            df["ARWU"] * w_arwu
    )

    df["Final Score"] = df["Final Score"].round(2)

    df = df.sort_values("Final Score", ascending=False)
    df["Rank"] = range(1, len(df) + 1)

    df["QS"] = df["QS"].round(2)
    df["THE"] = df["THE"].round(2)
    df["ARWU"] = df["ARWU"].round(2)

    return df[["Rank", "University", "QS", "THE", "ARWU", "Final Score"]]