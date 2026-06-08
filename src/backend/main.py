"""
main.py - Backend FastAPI do AgroSentinela (v3: multi-ESP32 + previsao ao vivo)
- Varios campos (cada ESP32 = um campo)
- A previsao PARTE da leitura real do sensor (graficos reagem)
- Cronograma recalculado ao vivo por cultura (mesmo objetivo do AG)
- Cultura escolhida por campo via interface
Execucao: uvicorn main:app --reload --port 8000
"""
import os, csv, json, datetime as dt, urllib.request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "data"))
FRONT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))
ASSETS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "assets"))
PREVISAO = os.path.join(DATA_DIR, "previsao.json")
CULTURAS = os.path.join(DATA_DIR, "culturas.json")
CSV_HIST = os.path.join(DATA_DIR, "dados_climaticos.csv")
LAT, LON = -21.17, -47.81
GANHO_POR_MM = 0.012; DECAIMENTO = 0.04; MAX_MM_HORA = 8.0; HORAS = 24

app = FastAPI(title="AgroSentinela API", version="3.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
ALERTAS = []

def _ler_json(c):
    if not os.path.exists(c): return None
    with open(c, encoding="utf-8") as f: return json.load(f)

def carregar_culturas(): return _ler_json(CULTURAS) or {}

_prev = _ler_json(PREVISAO) or {}
SERIE_LSTM = _prev.get("previsao_umidade", [0.16]*HORAS)[:HORAS]
if len(SERIE_LSTM) < HORAS: SERIE_LSTM += [SERIE_LSTM[-1]]*(HORAS-len(SERIE_LSTM))
UMIDADE_LSTM_INICIAL = _prev.get("ultima_leitura", SERIE_LSTM[0])

def _leitura(u, t=29.0, ar=45.0):
    return {"umidade_solo":u,"temperatura":t,"umidade_ar":ar,
            "timestamp":dt.datetime.now().isoformat(timespec="seconds")}

NOMES_CAMPOS = {"campo-soja":"Campo da Soja","campo-milho":"Campo do Milho",
                "campo-arroz":"Varzea (Arroz)","campo-cafe":"Sitio do Cafe"}
DISPOSITIVOS = {}

def previsao_ao_vivo(u):
    d = u - SERIE_LSTM[0]
    return [max(0.03, round(v+d, 4)) for v in SERIE_LSTM]

def cronograma_ao_vivo(prev, alvo):
    irr, com, ef = [], [], 0.0
    for base in prev:
        ef *= (1-DECAIMENTO); us = base+ef; i = 0.0
        if us < alvo: i = min(MAX_MM_HORA, (alvo-us)/GANHO_POR_MM); ef += i*GANHO_POR_MM
        irr.append(round(i,2)); com.append(round(base+ef,4))
    return irr, com

def detalhe_campo(dev_id):
    culturas = carregar_culturas(); dev = DISPOSITIVOS.get(dev_id)
    if not dev: return None
    cfg = culturas.get(dev["cultura"], {})
    crit = cfg.get("umidade_critica", 0.20); alvo = cfg.get("umidade_alvo", 0.26)
    u = dev["leitura"]["umidade_solo"]; prev = previsao_ao_vivo(u)
    irr, com = cronograma_ao_vivo(prev, alvo)
    risco = [i for i,v in enumerate(prev) if v < crit]
    return {"id":dev_id,"nome":dev["nome"],"cultura":dev["cultura"],
            "cultura_nome":cfg.get("nome",dev["cultura"]),"emoji":cfg.get("emoji","🌱"),
            "obs":cfg.get("obs",""),"umidade_critica":crit,"umidade_alvo":alvo,
            "umidade_atual":u,"leitura":dev["leitura"],"previsao_umidade":prev,
            "cronograma_mm_por_hora":irr,"umidade_com_irrigacao":com,
            "horas_em_risco":risco,"total_agua_mm":round(sum(irr),1),"em_risco":len(risco)>0}

def clima_atual():
    url = ("https://api.open-meteo.com/v1/forecast?latitude="+str(LAT)+"&longitude="+str(LON)+
           "&current=temperature_2m,relative_humidity_2m,precipitation,soil_moisture_3_to_9cm"
           "&timezone=America/Sao_Paulo")
    try:
        with urllib.request.urlopen(url, timeout=8) as r: c = json.loads(r.read())["current"]
        return {"fonte":"Open-Meteo (tempo real)","horario":c.get("time"),
                "temperatura":c.get("temperature_2m"),"umidade_ar":c.get("relative_humidity_2m"),
                "precipitacao":c.get("precipitation"),"umidade_solo":c.get("soil_moisture_3_to_9cm")}
    except Exception:
        return {"fonte":"offline","temperatura":None,"umidade_ar":None,"precipitacao":None,"umidade_solo":None}

class Leitura(BaseModel):
    id_fazenda: str; umidade_solo: float; temperatura: float
    umidade_ar: float; cultura: str = "soja"

class CulturaCampo(BaseModel):
    id: str; cultura: str

@app.get("/")
def raiz(): return {"servico":"AgroSentinela API","status":"online","versao":"3.0"}

@app.get("/api/culturas")
def get_culturas(): return carregar_culturas()

@app.get("/api/atual")
def get_atual(): return clima_atual()

@app.get("/api/dispositivos")
def get_dispositivos():
    lista = []
    for dev_id in DISPOSITIVOS:
        d = detalhe_campo(dev_id)
        lista.append({"id":d["id"],"nome":d["nome"],"cultura":d["cultura"],
            "cultura_nome":d["cultura_nome"],"emoji":d["emoji"],"umidade_atual":d["umidade_atual"],
            "umidade_critica":d["umidade_critica"],"umidade_alvo":d["umidade_alvo"],
            "em_risco":d["em_risco"],"total_agua_mm":d["total_agua_mm"],"timestamp":d["leitura"]["timestamp"]})
    return {"total":len(lista),"dispositivos":lista,"clima_atual":clima_atual()}

@app.get("/api/campo")
def get_campo(id: str):
    d = detalhe_campo(id); return d or {"erro":"campo nao encontrado"}

@app.post("/api/campo/cultura")
def set_cultura(req: CulturaCampo):
    culturas = carregar_culturas()
    if req.cultura not in culturas: return {"erro":"cultura invalida"}
    if req.id not in DISPOSITIVOS:
        DISPOSITIVOS[req.id] = {"nome":NOMES_CAMPOS.get(req.id, req.id), "leitura":_leitura(UMIDADE_LSTM_INICIAL)}
    DISPOSITIVOS[req.id]["cultura"] = req.cultura; DISPOSITIVOS[req.id]["fixada"] = True
    return {"ok":True,"id":req.id,"cultura":req.cultura}

def disparar_alerta(msg, dev_id, cultura, u):
    a = {"timestamp":dt.datetime.now().isoformat(timespec="seconds"),"campo":dev_id,
         "cultura":cultura,"umidade_solo":u,"mensagem":msg,"canal":"SNS (simulado) -> SMS/voz"}
    ALERTAS.append(a); print("[SNS-SIMULADO] " + msg); return a

@app.post("/api/leitura")
def post_leitura(leitura: Leitura):
    dev_id = leitura.id_fazenda; culturas = carregar_culturas()
    dev = DISPOSITIVOS.get(dev_id, {"fixada": False})
    if not dev.get("fixada"):
        dev["cultura"] = leitura.cultura if leitura.cultura in culturas else "soja"
    dev.setdefault("cultura", "soja")
    dev["nome"] = dev.get("nome") or NOMES_CAMPOS.get(dev_id, dev_id)
    dev["leitura"] = {"umidade_solo":leitura.umidade_solo,"temperatura":leitura.temperatura,
                      "umidade_ar":leitura.umidade_ar,"timestamp":dt.datetime.now().isoformat(timespec="seconds")}
    DISPOSITIVOS[dev_id] = dev
    cfg = culturas.get(dev["cultura"], {}); crit = cfg.get("umidade_critica", 0.20)
    em_risco = leitura.umidade_solo < crit
    resp = {"recebido":True,"campo":dev_id,"cultura":dev["cultura"],"em_risco":em_risco}
    if em_risco:
        msg = ("Risco hidrico no campo "+dev["nome"]+" ("+cfg.get("nome",dev["cultura"])+
               "): umidade "+format(leitura.umidade_solo,".3f")+" abaixo do limiar "+str(crit)+".")
        resp["alerta"] = disparar_alerta(msg, dev_id, dev["cultura"], leitura.umidade_solo)
    return resp

@app.get("/api/alertas")
def get_alertas(): return {"total":len(ALERTAS),"alertas":ALERTAS[-20:]}



if os.path.isdir(FRONT_DIR):
    app.mount("/app", StaticFiles(directory=FRONT_DIR, html=True), name="app")
