"""
coleta_dados.py - AgroSentinela
Coleta dados climaticos e de umidade do solo REAIS da API Open-Meteo
(historica, gratuita, sem cadastro) para Ribeirao Preto/SP e gera o CSV
usado pelos demais modulos. Cap. 1 (consolidacao de sistema).
"""
import os, argparse, datetime as dt
import requests, pandas as pd

REGIAO_PADRAO = {"nome": "Ribeirao Preto - SP", "latitude": -21.17, "longitude": -47.81}
VARIAVEIS_HORARIAS = [
    "temperature_2m", "relative_humidity_2m", "precipitation",
    "et0_fao_evapotranspiration", "soil_temperature_0_to_7cm",
    "soil_moisture_0_to_7cm", "soil_moisture_7_to_28cm",
]
URL_OPEN_METEO = "https://archive-api.open-meteo.com/v1/archive"


def coletar(latitude, longitude, data_inicio, data_fim, timeout=60):
    parametros = {
        "latitude": latitude, "longitude": longitude,
        "start_date": data_inicio, "end_date": data_fim,
        "hourly": ",".join(VARIAVEIS_HORARIAS), "timezone": "America/Sao_Paulo",
    }
    resposta = requests.get(URL_OPEN_METEO, params=parametros, timeout=timeout)
    resposta.raise_for_status()
    df = pd.DataFrame(resposta.json()["hourly"])
    df["time"] = pd.to_datetime(df["time"])
    return df.sort_values("time").reset_index(drop=True)


def enriquecer(df):
    LIMIAR = 0.20  # m3/m3 - ponto de alerta de estresse hidrico
    df = df.copy()
    df["risco_hidrico"] = (df["soil_moisture_0_to_7cm"] < LIMIAR).astype(int)
    df["hora"] = df["time"].dt.hour
    df["dia_do_ano"] = df["time"].dt.dayofyear
    return df


def salvar_csv(df, caminho):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    df.to_csv(caminho, index=False)
    print("[OK] " + str(len(df)) + " registros salvos em: " + caminho)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lat", type=float, default=REGIAO_PADRAO["latitude"])
    p.add_argument("--lon", type=float, default=REGIAO_PADRAO["longitude"])
    p.add_argument("--inicio", default=None)
    p.add_argument("--fim", default=None)
    p.add_argument("--saida", default=os.path.join(os.path.dirname(__file__), "..", "..", "data", "dados_climaticos.csv"))
    a = p.parse_args()
    hoje = dt.date.today()
    fim = a.fim or (hoje - dt.timedelta(days=2)).isoformat()
    inicio = a.inicio or (hoje - dt.timedelta(days=730)).isoformat()
    print("[INFO] Coletando " + REGIAO_PADRAO["nome"] + " (" + str(a.lat) + ", " + str(a.lon) + ")")
    print("[INFO] Periodo: " + inicio + " -> " + fim)
    df = enriquecer(coletar(a.lat, a.lon, inicio, fim))
    salvar_csv(df, os.path.abspath(a.saida))
    print("[RESUMO] umidade media solo: " + format(df["soil_moisture_0_to_7cm"].mean(), ".3f") + " m3/m3")


if __name__ == "__main__":
    main()
