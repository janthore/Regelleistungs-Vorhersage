import pandas as pd
import numpy as np
from bachelorarbeit import config
from datetime import date
import os
from bachelorarbeit import config
from tqdm import tqdm

path = os.path.dirname(os.path.abspath(__file__))


def get_gradient(start: date, end: date, ünb=config.ünb, sort=False) -> pd.DataFrame:
    if isinstance(ünb, str):
        ünb_list = [ünb]
    else:
        ünb_list = ünb
    daten = []
    for unb in tqdm(ünb_list, desc="Gradienten laden"):
        file_path = os.path.join(path, f"Gradienten_{unb}.csv")
        df = pd.read_csv(file_path, index_col=0, parse_dates=True, dayfirst=True)
        df = config.format_date(df)
        df = df.loc[start:end]
        daten.append(df)
    df_gesamt = pd.concat(daten, axis=1)
    if sort:
        df_gesamt = sort_by_PSRType(df_gesamt)
    return df_gesamt

def sort_by_PSRType(df: pd.DataFrame) -> pd.DataFrame:
    mapping = pd.Series(df.columns.str.extract(r"^(B\d{2})")[0].values, index=df.columns)
    mapping = mapping.dropna()
    df_valid = df[mapping.index]
    df_grouped = df_valid.T.groupby(mapping).sum().T
    return df_grouped




if __name__ == "__main__":
    print(get_gradient(config.Config.start_date, config.Config.end_date, sort=True))

