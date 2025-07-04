from entsoe import EntsoePandasClient
import pandas as pd

# Initialisiere Client mit deinem API-Key
client = EntsoePandasClient(api_key="c5a9c2a8-1655-432a-9e59-c9f035af22db")
#"DE_50HZ"
ünb = [ "DE_TENNET", "DE_AMPRION", "DE_TRANSNET"]
ünb1 = ["DE_50HZ","DE_TENNET", "DE_AMPRION", "DE_TRANSNET"]
#DE_50HZ
#DE_TENNET
#DE_AMPRION
#DE_TRANSNET
def get_entsoe_data(data_type: str, country_code: str, start_date: str, end_date: str):
    """
    Lädt ENTSO-E Daten via entsoe-py.

    Parameters:
    - data_type: "load", "generation", "day_ahead_prices", "wind_solar_forecast", ...
    - country_code: z. B. "DE_LU", "FR", "AT"
    - start_date, end_date: Datum als 'YYYY-MM-DD'

    Returns:
    - pd.DataFrame oder pd.Series mit den Daten
    """
    start = pd.Timestamp(start_date, tz="UTC")
    end = pd.Timestamp(end_date, tz="UTC")

    if data_type == "load":
        return client.query_load(country_code, start=start, end=end)

    elif data_type == "generation":
        return client.query_generation(country_code, start=start, end=end)

    elif data_type == "day_ahead_prices":
        return client.query_day_ahead_prices(country_code, start=start, end=end)

    elif data_type == "wind_solar_forecast":
        return client.query_wind_and_solar_forecast(country_code, start=start, end=end)

    elif data_type == "load_forecast":
        return client.query_load_forecast(country_code, start=start, end=end)

    elif data_type == "installed_generation_capacity":
        return client.query_installed_generation_capacity(country_code, start=start, end=end)
    elif data_type == "generation_forecast":
        return client.query_generation_forecast(country_code, start=start, end=end)
    elif data_type == "generation_wind_solar_forecast":
        return client.query_wind_and_solar_forecast(country_code, start=start, end=end, psr_type=None)
    elif data_type == "unavailability_generation_units":
        return client.query_unavailability_of_generation_units(country_code, start=start, end=end, docstatus=None,
                                                        periodstartupdate=None, periodendupdate=None)
    elif data_type == "unavailability_of_production_unit":
        print(f"Abfrage: {data_type}")
        return client.query_unavailability_of_production_units(country_code, start, end, docstatus=None,
                                                        periodstartupdate=None, periodendupdate=None)

    else:
        raise ValueError(f"Unbekannter Datentyp: {data_type}")


if __name__ == "__main__":
    from datetime import date
    start_date = date(2025, 5, 1)
    end_date = date(2025, 6, 1)
    ausfälle = get_entsoe_data("unavailability_of_generation_unit",ünb[0], start_date, end_date)
    ausfälle.to_csv("ausfälle.csv", index=True)