from datetime import date, datetime

start_date = date(2020, 1, 1)
end_date = date(2025, 5, 1)

import requests
import pandas as pd
import os

pfad = os.path.abspath(__file__)
pfad_ordner = os.path.dirname(pfad)



def get_weather_data(lat, lon, start_date, end_date, parameter, interpolate=True):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "hourly": ",".join(parameter),
        "timezone": "Europe/Berlin"
    }

    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data["hourly"])
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)
    wetter = df
    if interpolate:
        wetter = wetter.resample("15min").interpolate(method="linear") #Achtung die Daten werden hier auf 15 Minuten hoch skalliert über die lineare Methode
    wetter.index.name = "timestamp"
    wetter.index = pd.to_datetime(wetter.index)
    wetter.index = wetter.index.tz_localize("UTC")
    return wetter


wind = ["wind_speed_100m",
            "wind_gusts_10m",
            ]      # Böen nur in 10 m verfügbar
solar = ["cloudcover",
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            ]



# Beispiel: Berlin, 1. bis 7. April 2024
# wind_daten = get_weather_data(wind_deutschland[0], wind_deutschland[1], start_date,end_date , wind)
# wind_daten.to_csv("wetterparameter_wind.csv")
# solar_daten = get_weather_data(solar_deutschland[0], solar_deutschland[1], start_date,end_date , solar)
# solar_daten.to_csv("wetterparameter_solar.csv")

# print(wind_daten.columns)
# print(solar_daten.columns)

def get_weather_data_solar(start_date: date, end_date: date, interpolate=True) -> pd.DataFrame:
    file_path = os.path.join(pfad_ordner, "Wetterpunkte_PV.csv")
    df = pd.read_csv(file_path)
    all_data = pd.DataFrame()

    for _, row in df.iterrows():
        station_name = row["Name"]
        solar_daten = get_weather_data(
            float(row["Lat"]),
            float(row["Lon"]),
            start_date,
            end_date,
            solar,
            interpolate=interpolate
        )

        # Spalten umbenennen
        solar_daten = solar_daten.add_suffix(f"_{station_name}")
        solar_daten.index.name = "timestamp"

        # Merge mit Haupt-DataFrame
        if all_data.empty:
            all_data = solar_daten
        else:
            all_data = all_data.merge(solar_daten, left_index=True, right_index=True, how="outer")

    return all_data


def get_weather_data_wind(start_date: date, end_date: date, interpolate=True) -> pd.DataFrame:
    file_path = os.path.join(pfad_ordner, "Wetterpunkte_Wind.csv")
    df = pd.read_csv(file_path)
    all_data = pd.DataFrame()
    for _, row in df.iterrows():
        stationsname = row["Name"]
        wind_daten = get_weather_data(float(row['Lat']), float(row['Lon']), start_date,end_date , wind, interpolate=interpolate)
        wind_daten = wind_daten.add_suffix(f"_{stationsname}")
        if all_data.empty:
            all_data = wind_daten
        else:
            all_data = all_data.merge(wind_daten, left_index=True, right_index=True, how="outer")
    return all_data

def get_total_weather_data_for_germany(start_date: date, end_date: date, interpolate=True) -> pd.DataFrame:
    wind_daten = get_weather_data_wind(start_date, end_date, interpolate=interpolate)
    solar_daten = get_weather_data_solar(start_date, end_date, interpolate=interpolate)
    return wind_daten.join(solar_daten)


import pandas as pd
import re

import pandas as pd
import re
# Diese Funktion wurde mal für eine alte Variante benötigt hat jetzt aber keine verwendung mehr
""""
def summarize_by_variable_over_time(df: pd.DataFrame) -> pd.DataFrame:
    dfr = pd.DataFrame()
    spalten = wind + solar
    for spalte in spalten:
        # Filtere alle Spalten, die den aktuellen Variablennamen enthalten
        relevant_cols = [col for col in df.columns if spalte in col]
        relevant_cols = sorted(relevant_cols)

        # Statistiken berechnen
        dfr[f'{spalte}_Mean'] = df[relevant_cols].mean(axis=1)
        dfr[f'{spalte}_Var'] = df[relevant_cols].var(axis=1) #Achtung die Varianz ist hier unpassend bei einigen Prozentualen werten !!!
        dfr[f'{spalte}_Min'] = df[relevant_cols].min(axis=1)
        dfr[f'{spalte}_Max'] = df[relevant_cols].max(axis=1)
    return dfr
"""

if __name__ == "__main__":
    df_wind = get_weather_data_wind(date(2024, 1, 1), date(2024, 1, 5))
    df_solar = get_weather_data_solar(date(2024, 1, 1), date(2024, 1, 5))
    print(df_wind.head())