#Speichern von Kinfiguarationsvariablen welche immer wieder vorkommen
from dataclasses import dataclass
from datetime import date
import pandas as pd
@dataclass(frozen=True)
class Config:
    seed: int = 42
    start_date: pd.Timestamp = pd.Timestamp(date(2020, 1, 1)).tz_localize("UTC")
    end_date: pd.Timestamp = pd.Timestamp(date(2025, 5, 1)).tz_localize("UTC")

#Übertragungsnetzbetreiber in Deutschland
ünb = ["DE_50HZ", "DE_TENNET", "DE_AMPRION", "DE_TRANSNET"]


#Farbschema für Plots
PLOT_COLORS = {
    "50HZ": "blue",
    "TENNET": "orange",
    "AMPRION": "purple",
    "TRANSNET": "green",
}



import pandas as pd

def format_date(df):
    # Versuche automatische Konvertierung, egal welches Format
    df.index = pd.to_datetime(df.index, utc=True, errors="raise")
    df.index = df.index.tz_convert("UTC")
    return df

PSRTYPE = {
    'A03': 'Mixed',
    'A04': 'Generation',
    'A05': 'Load',
    'B01': 'Biomass',
    'B02': 'Fossil Brown coal/Lignite',
    'B03': 'Fossil Coal-derived gas',
    'B04': 'Fossil Gas',
    'B05': 'Fossil Hard coal',
    'B06': 'Fossil Oil',
    'B07': 'Fossil Oil shale',
    'B08': 'Fossil Peat',
    'B09': 'Geothermal',
    'B10': 'Hydro Pumped Storage',
    'B11': 'Hydro Run-of-river and poundage',
    'B12': 'Hydro Water Reservoir',
    'B13': 'Marine',
    'B14': 'Nuclear',
    'B15': 'Other renewable',
    'B16': 'Solar',
    'B17': 'Waste',
    'B18': 'Wind Offshore',
    'B19': 'Wind Onshore',
    'B20': 'Other',
    'B21': 'AC Link',
    'B22': 'DC Link',
    'B23': 'Substation',
    'B24': 'Transformer',
    'B25': 'Energy storage'
}