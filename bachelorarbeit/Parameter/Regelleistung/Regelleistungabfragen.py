import requests
import pandas as pd
from io import StringIO
client_id = "cm_app_ntp_id_549f67fe4e874e85ab341a45801a7749"
client_secret = "ntp_PXkd4VddarVlhcAmOTHq"
#In diesem Dokument kann die Verwendete Regelleistung abgefragt werden
import requests
import sys
import os
import numpy as np
ünb = [
    "50Hertz (Positiv)",
    "Amprion (Positiv)",
    "TenneT TSO (Positiv)",
    "TransnetBW (Positiv)",
    "50Hertz (Negativ)",
    "Amprion (Negativ)",
    "TenneT TSO (Negativ)",
    "TransnetBW (Negativ)",
]
deutschland = ['Deutschland (Positiv)', 'Deutschland (Negativ)']

spalten = ünb + deutschland
def new_token():
    # add your Client-ID and Client-secret from the API Client configuration GUI to
    # your environment variable first
    IPNT_CLIENT_ID = client_id
    IPNT_CLIENT_SECRET = client_secret
    
    ACCESS_TOKEN_URL = "https://identity.netztransparenz.de/users/connect/token"
    
    
    
    # Ask for the token providing above authorization data
    response = requests.post(ACCESS_TOKEN_URL,
                    data = {
                            'grant_type': 'client_credentials',
                            'client_id': IPNT_CLIENT_ID,
                            'client_secret': IPNT_CLIENT_SECRET
            })
    
    # Parse the token from the response if the response was OK 
    if response.ok:
        token = response.json()['access_token']
    else:
        print(f'Error retrieving token\n{response.status_code}:{response.reason}',
            file = sys.stderr)
        exit(-1)
    
    # Provide URL to request health info on API
    myURL = "https://ds.netztransparenz.de/api/v1/health"
    response = requests.get(myURL, headers = {'Authorization': 'Bearer {}'.format(token)})
    print(response.text, file = sys.stdout)
    return token




def daten_abfrage_netztranzparenz(dateFrom, dateTo, produkt): #dateFrom, dateTo, Produkt
    token = new_token()

    url = f"https://ds.netztransparenz.de/{abfrage_Adresse(produkt)}/{dateFrom.isoformat()}/{dateTo.isoformat()}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "text/csv"  # <- KORREKT für diese API
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        csv_text = response.text
        df = pd.read_csv(StringIO(csv_text), sep=';', decimal=',')
        df = timespamp_anfuegen(df)
        df = df.astype(str)
        df = df.replace("N.A.", np.nan)
        df = df.replace("", np.nan)
        df.dropna(inplace=True)
        df = df.apply(lambda col: col.str.replace(",", ".", regex=False))
        df = df.apply(pd.to_numeric, errors="coerce")
        return df
        
        
    else:
        raise RuntimeError(f"❌ Fehler bei Datenabfrage ({response.status_code}):\n{response.text}")
    
def abfrage_Adresse(produkt):
    datenquellen = {
    # für diese Arbeit relevante Quellen
    "aFRR-Optimierung qualitätsgesichert": "api/v1/data/NrvSaldo/SRLOptimierung/Qualitaetsgesichert",
    "aFRR-Optimierung betrieblich": "api/v1/data/NrvSaldo/SRLOptimierung/Betrieblich",
    "Aktivierte aFRR qualitätsgesichert": "api/v1/data/NrvSaldo/AktivierteSRL/Qualitaetsgesichert",
    "Aktivierte aFRR betrieblich": "api/v1/data/NrvSaldo/AktivierteSRL/Betrieblich",
    "Aktivierte mFRR qualitätsgesichert": "api/v1/data/NrvSaldo/AktivierteMRL/Qualitaetsgesichert",
    "Aktivierte mFRR betrieblich": "api/v1/data/NrvSaldo/AktivierteMRL/Betrieblich",
    "mFRR-Optimierung qualitätsgesichert": "api/v1/data/NrvSaldo/MRLOptimierung/Qualitaetsgesichert",
    "mFRR-Optimierung betrieblich": "api/v1/data/NrvSaldo/MRLOptimierung/Betrieblich",
    "Solarenergie Prognose": "api/v1/data/prognose/Solar",
    "Windenergie Prognose": "api/v1/data/prognose/Wind",
    "Solarenergie Hochrechnung": "api/v1/data/hochrechnung/Solar",
    "Windenergie Hochrechnung": "api/v1/data/hochrechnung/Wind",

    # Alle weiteren Quellen der API
    "1/4h-Auktion EPEX": "api/v1/data/vermarktung/VermarktungEpex",
    "1/4h-Auktion EXAA": "api/v1/data/vermarktung/VermarktungExaa",
    "Abregelungsstrommenge ausgewiesen": "api/v1/data/AusgewieseneABSM",
    "Abregelungsstrommenge zugeteilt": "api/v1/data/ZugeteilteABSM",
    "Abregelungsstrommenge Erzeugungsverbot": "api/v1/data/Erzeugungsverbot",
    "Abschaltbare Lasten qualitätsgesichert": "api/v1/data/NrvSaldo/AbschaltbareLasten/Qualitaetsgesichert",
    "Abschaltbare Lasten betrieblich": "api/v1/data/NrvSaldo/AbschaltbareLasten/Betrieblich",
    "AEP-Modul": "api/v1/data/NrvSaldo/AEPModule/Qualitaetsgesichert",
    "AepSchaetzer": "api/v1/data/NrvSaldo/AepSchaetzer/Betrieblich",
    "Difference qualitätsgesichert": "api/v1/data/NrvSaldo/Difference/Qualitaetsgesichert",
    "Difference betrieblich": "api/v1/data/NrvSaldo/Difference/Betrieblich",
    "Differenz Einspeiseprognose": "api/v1/data/vermarktung/DifferenzEinspeiseprognose",
    "Finanzielle Wirkung AEP": "api/v1/data/NrvSaldo/FinanzielleWirkungAEPModule/Qualitaetsgesichert",
    "Inanspruchnahme Ausgleichsenergie": "api/v1/data/vermarktung/InanspruchnahmeAusgleichsenergie",
    "Index Ausgleichsenergiepreis (ID-AEP)": "api/v1/data/IdAep",
    "Jahresmarktwerte": "api/v1/data/Jahresmarktpraemie",
    "Kapazitätsreserve": "api/v1/data/Kapazitaetsreserve",
    "Monatsmarktwerte": "api/v1/data/marktpraemie",
    "MOL-Abweichungen SRL": "api/v1/data/NrvSaldo/SrlMolAbweichungen/Betrieblich",
    "MOL-Abweichungen MRL": "api/v1/data/NrvSaldo/MrlMolAbweichungen/Betrieblich",
    "Negative Preise (1h)": "api/v1/data/NegativePreise/1",
    "Negative Preise (3h)": "api/v1/data/NegativePreise/3",
    "Negative Preise (4h)": "api/v1/data/NegativePreise/4",
    "Negative Preise (6h)": "api/v1/data/NegativePreise/6",
    "Nothilfe Ausland qualitätsgesichert": "api/v1/data/NrvSaldo/Nothilfe/Qualitaetsgesichert",
    "NRV-Saldo qualitätsgesichert": "api/v1/data/NrvSaldo/NRVSaldo/Qualitaetsgesichert",
    "NRV-Saldo betrieblich": "api/v1/data/NrvSaldo/NRVSaldo/Betrieblich",
    "NRV-Saldo-Ampel": "api/v1/data/Trafficlight",
    "OnlineHochrechnung Solar": "api/v1/data/onlinehochrechnung/Solar",
    "OnlineHochrechnung Wind Onshore": "api/v1/data/onlinehochrechnung/Windonshore",
    "OnlineHochrechnung Wind Offshore": "api/v1/data/onlinehochrechnung/Windoffshore",
    "PRL (k * Delta f) qualitätsgesichert": "api/v1/data/NrvSaldo/PRL/Qualitaetsgesichert",
    "PRL (k * Delta f) betrieblich": "api/v1/data/NrvSaldo/PRL/Betrieblich",
    "reBAP": "api/v1/data/NrvSaldo/reBAP/Qualitaetsgesichert",
    "Redispatch": "api/v1/data/redispatch",
    "RZ-Saldo qualitätsgesichert": "api/v1/data/NrvSaldo/RZSaldo/Qualitaetsgesichert",
    "RZ-Saldo betrieblich": "api/v1/data/NrvSaldo/RZSaldo/Betrieblich",
    "Spotmarktpreise": "api/v1/data/Spotmarktpreise",
    "Untertägige Strommengen": "api/v1/data/vermarktung/UntertaegigeStrommengen",
    "Vermarktungsprognose Solarenergie": "api/v1/data/vermarktung/VermarktungsSolar",
    "Vermarktungsprognose Sonstige": "api/v1/data/vermarktung/VermarktungsSonstige",
    "Vermarktungsprognose Windenergie": "api/v1/data/vermarktung/VermarktungsWind",
    "VoAA": "api/v1/data/NrvSaldo/VoAA/Qualitaetsgesichert",
    "Zusatzmaßnahmen qualitätsgesichert": "api/v1/data/NrvSaldo/Zusatzmassnahmen/Qualitaetsgesichert",
    "Zusatzmaßnahmen betrieblich": "api/v1/data/NrvSaldo/Zusatzmassnahmen/Betrieblich"
    }
    return datenquellen.get(produkt)
from pathlib import Path
pfad_aFRR = r"C:\Users\janth\OneDrive\Desktop\Studium\Bachelorarbeit\Regelleistungs_Vorhersage\bachelorarbeit\Parameter\Regelleistung\Aktivierte aFRR qualitaetsgesichert alle Daten.csv"
pfad_mFRR = r"C:\Users\janth\OneDrive\Desktop\Studium\Bachelorarbeit\Regelleistungs_Vorhersage\bachelorarbeit\Parameter\Regelleistung\Aktivierte mFRR qualitaetsgesichert alle Daten.csv"

def get_regelleistung(start_date, end_date):
    df_aFRR = tabelle_aufbereiten(start_date, end_date, pfad_aFRR)
    df_mFRR = tabelle_aufbereiten(start_date, end_date, pfad_mFRR)
    return df_aFRR + df_mFRR

def tabelle_aufbereiten(start_date, end_date, pfad) -> pd.DataFrame:
    """
    Bereitet die Zeilen des DataFrames auf, indem sie in numerische Werte umgewandelt werden.
    """
    base_dir = Path(__file__).parent  # Ordner, in dem die aktuelle Datei liegt
    full_path = base_dir / pfad
    df = pd.read_csv(full_path, sep=';', decimal=',')

    df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y', errors='coerce')
    df = df.loc[(df['Datum'] >= start_date.strftime('%d.%m.%Y')) & (df['Datum'] <= end_date.strftime('%d.%m.%Y'))]
    df['Datum'] = df['Datum'].dt.strftime('%d.%m.%Y')  # Formatieren des Datums zurück zu String
    df = timespamp_anfuegen(df)
    df = df[spalten]
    zeilen = len(df)
    df = df.astype(str)
    df = df.apply(lambda col: col.str.replace(",", ".", regex=False))
    df = df.apply(pd.to_numeric, errors="coerce")
    df = df.astype(float)
    df = df.replace("N.A." , np.nan)
    df = df.replace("NaN", np.nan)
    df = df.replace("", np.nan)
    df = df.dropna()
    print(f"Zeilen fallen gelassen: {zeilen - len(df)} von {zeilen} Zeilen")
    return df



def timespamp_anfuegen(tabelle):
    tabelle['timestamp'] = tabelle['Datum'] + ' ' + tabelle['von']
    tabelle['timestamp'] = pd.to_datetime(tabelle['timestamp'], format='%d.%m.%Y %H:%M')
    tabelle['timestamp'] = tabelle['timestamp'].dt.tz_localize('UTC')
    tabelle = tabelle.set_index('timestamp')
    return tabelle

# from datetime import date

# start_date = date(2025, 1, 1)
# end_date = date(2025, 1, 5)
# gesamtrückgabe = daten_abfrage_netztranzparenz(start_date, end_date,"Aktivierte aFRR betrieblich")
# print(gesamtrückgabe.head())
from datetime import date

if __name__ == "__main__":
    start = date(2014, 1, 1)
    end = date(2025, 1, 1)
    test = get_regelleistung(start, end)
    print(test.describe())
    print(test.index.dtype)