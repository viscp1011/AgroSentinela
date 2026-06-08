"""
modelo_lstm.py - AgroSentinela
Rede Neural Recorrente (LSTM, Keras/TensorFlow) que preve a umidade do solo
das proximas horas a partir do historico real. Cap. 2 (RNN).
Saidas: modelo_lstm.keras, scaler.pkl, previsao.json, assets/grafico_previsao.png
"""
import os, json, pickle
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "data"))
ASSETS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "assets"))
CSV_ENTRADA = os.path.join(DATA_DIR, "dados_climaticos.csv")
MODELO_SAIDA = os.path.join(DATA_DIR, "modelo_lstm.keras")
SCALER_SAIDA = os.path.join(DATA_DIR, "scaler.pkl")
PREVISAO_SAIDA = os.path.join(DATA_DIR, "previsao.json")
GRAFICO_SAIDA = os.path.join(ASSETS_DIR, "grafico_previsao.png")

FEATURES = ["temperature_2m","relative_humidity_2m","precipitation",
            "et0_fao_evapotranspiration","soil_temperature_0_to_7cm",
            "soil_moisture_0_to_7cm","soil_moisture_7_to_28cm"]
ALVO = "soil_moisture_0_to_7cm"; IDX_ALVO = FEATURES.index(ALVO)
JANELA = 24; LIMIAR_CRITICO = 0.20
EPOCAS = int(os.environ.get("AGRO_EPOCAS", "30"))
BATCH = int(os.environ.get("AGRO_BATCH", "64"))


def criar_janelas(m, janela, idx):
    X, y = [], []
    for i in range(len(m) - janela):
        X.append(m[i:i+janela]); y.append(m[i+janela, idx])
    return np.array(X), np.array(y)


def construir_modelo(n):
    md = Sequential([Input(shape=(JANELA, n)), LSTM(64, return_sequences=True),
                     Dropout(0.2), LSTM(32), Dropout(0.2),
                     Dense(16, activation="relu"), Dense(1)])
    md.compile(optimizer="adam", loss="mse", metrics=["mae"])
    return md


def _desn(scaler, v):
    mn = scaler.data_min_[IDX_ALVO]; fx = scaler.data_max_[IDX_ALVO]-mn
    return v*fx+mn


def treinar():
    df = pd.read_csv(CSV_ENTRADA)
    dados = df[FEATURES].astype("float32").values
    scaler = MinMaxScaler(); dn = scaler.fit_transform(dados)
    X, y = criar_janelas(dn, JANELA, IDX_ALVO)
    corte = int(len(X)*0.8)
    md = construir_modelo(len(FEATURES))
    parada = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
    print("[INFO] Treinando LSTM...")
    md.fit(X[:corte], y[:corte], validation_split=0.1, epochs=EPOCAS,
           batch_size=BATCH, callbacks=[parada], verbose=2)
    _, mae = md.evaluate(X[corte:], y[corte:], verbose=0)
    print("[OK] MAE teste: " + format(mae*(scaler.data_max_[IDX_ALVO]-scaler.data_min_[IDX_ALVO]), ".4f") + " m3/m3")
    md.save(MODELO_SAIDA)
    with open(SCALER_SAIDA, "wb") as f: pickle.dump(scaler, f)
    _grafico(md, scaler, X[corte:], y[corte:])
    _prever(md, scaler, dn)


def _grafico(md, scaler, Xt, yt, n=200):
    pred = _desn(scaler, md.predict(Xt[-n:], verbose=0).flatten())
    real = _desn(scaler, yt[-n:])
    plt.figure(figsize=(11,4.5))
    plt.plot(real, label="Umidade real", linewidth=2)
    plt.plot(pred, "--", label="Umidade prevista (LSTM)", linewidth=2)
    plt.axhline(LIMIAR_CRITICO, color="red", linestyle=":", label="Limiar de risco")
    plt.title("AgroSentinela - Previsao de umidade do solo (LSTM) - Ribeirao Preto/SP")
    plt.xlabel("Horas (teste)"); plt.ylabel("Umidade 0-7cm (m3/m3)"); plt.legend()
    plt.tight_layout(); os.makedirs(ASSETS_DIR, exist_ok=True)
    plt.savefig(GRAFICO_SAIDA, dpi=120); plt.close()
    print("[OK] Grafico: " + GRAFICO_SAIDA)


def _prever(md, scaler, dn, horas=24):
    jan = dn[-JANELA:].copy(); out = []
    for _ in range(horas):
        p = md.predict(jan.reshape(1, JANELA, len(FEATURES)), verbose=0)[0,0]
        out.append(p); nl = jan[-1].copy(); nl[IDX_ALVO] = p
        jan = np.vstack([jan[1:], nl])
    prev = _desn(scaler, np.array(out))
    risco = [i for i,v in enumerate(prev) if v < LIMIAR_CRITICO]
    res = {"regiao":"Ribeirao Preto - SP",
           "ultima_leitura": float(_desn(scaler, dn[-1, IDX_ALVO])),
           "limiar_critico": LIMIAR_CRITICO, "horizonte_horas": horas,
           "previsao_umidade":[round(float(v),4) for v in prev],
           "horas_em_risco": risco,
           "primeira_hora_risco": (risco[0] if risco else None)}
    with open(PREVISAO_SAIDA, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    print("[OK] Previsao 24h: " + PREVISAO_SAIDA)


if __name__ == "__main__":
    treinar()
