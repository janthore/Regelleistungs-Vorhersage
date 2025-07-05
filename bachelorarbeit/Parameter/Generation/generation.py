import pandas as pd
from bachelorarbeit import config


path = r"C:\Users\janth\OneDrive\Desktop\Studium\Bachelorarbeit\Regelleistungs_Vorhersage\bachelorarbeit\Parameter\Generation\generation_2019_bis_heute.csv"

def get_generation(start_date, end_date):
    """
    Liest die Generationsdaten aus der CSV-Datei und filtert sie nach dem angegebenen Zeitraum.

    Parameter:
    -----------
    start_date : str
        Startdatum im Format 'YYYY-MM-DD'.
    end_date : str
        Enddatum im Format 'YYYY-MM-DD'.

    Rückgabe:
    ---------
    pd.DataFrame
        Gefilterter DataFrame mit den Generationsdaten.
    """
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    df = df[(df.index >= start_date) & (df.index <= end_date)]
    return df

if __name__ == "__main__":
    print(get_generation(start_date="2019-01-01", end_date="2019-12-31"))