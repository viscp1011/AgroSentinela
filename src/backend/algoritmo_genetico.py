"""
algoritmo_genetico.py - AgroSentinela
Algoritmo Genetico (DEAP) que otimiza o cronograma de irrigacao de 24h por
CULTURA (agua x risco). Cap. 4. Le previsao.json (LSTM) e culturas.json.
Saida: cronograma_<cultura>.json + assets/grafico_irrigacao_<cultura>.png
"""
import os, sys, json, random
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "data"))
ASSETS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "assets"))
PREVISAO = os.path.join(DATA_DIR, "previsao.json")
CULTURAS = os.path.join(DATA_DIR, "culturas.json")

HORAS = 24; GANHO_POR_MM = 0.012; DECAIMENTO = 0.04
MAX_MM_POR_HORA = 8.0; CUSTO_POR_MM = 1.0; PESO_DEFICIT = 250.0
UMIDADE_ALVO = 0.22; UMIDADE_BASE = np.linspace(0.21, 0.15, HORAS)


def carregar_culturas():
    with open(CULTURAS, encoding="utf-8") as f: return json.load(f)

def carregar_previsao():
    if os.path.exists(PREVISAO):
        with open(PREVISAO, encoding="utf-8") as f:
            return np.array(json.load(f)["previsao_umidade"], dtype=float)[:HORAS]
    return np.linspace(0.21, 0.15, HORAS)

def simular_umidade(irrig):
    u = np.empty(HORAS); ef = 0.0
    for t in range(HORAS):
        ef = ef*(1-DECAIMENTO) + irrig[t]*GANHO_POR_MM; u[t] = UMIDADE_BASE[t]+ef
    return u

def avaliar(ind):
    ir = np.array(ind); u = simular_umidade(ir)
    custo = float(np.sum(ir))*CUSTO_POR_MM
    deficit = np.maximum(0.0, UMIDADE_ALVO-u)
    return (custo + float(np.sum(deficit))*PESO_DEFICIT,)

if not hasattr(creator, "FitnessMin"):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
if not hasattr(creator, "Individuo"):
    creator.create("Individuo", list, fitness=creator.FitnessMin)

def construir_toolbox():
    tb = base.Toolbox()
    tb.register("gene", random.uniform, 0.0, MAX_MM_POR_HORA)
    tb.register("individuo", tools.initRepeat, creator.Individuo, tb.gene, n=HORAS)
    tb.register("populacao", tools.initRepeat, list, tb.individuo)
    tb.register("evaluate", avaliar); tb.register("mate", tools.cxBlend, alpha=0.5)
    tb.register("mutate", tools.mutGaussian, mu=0.0, sigma=1.0, indpb=0.2)
    tb.register("select", tools.selTournament, tournsize=3)
    return tb

def _corrigir(pop):
    for ind in pop:
        for i in range(len(ind)): ind[i] = min(MAX_MM_POR_HORA, max(0.0, ind[i]))

def otimizar(alvo, geracoes=60, tam_pop=120, semente=42):
    global UMIDADE_ALVO; UMIDADE_ALVO = alvo
    random.seed(semente); np.random.seed(semente)
    tb = construir_toolbox(); pop = tb.populacao(n=tam_pop); hof = tools.HallOfFame(1)
    for ind in pop: ind.fitness.values = tb.evaluate(ind)
    hof.update(pop)
    for _ in range(geracoes):
        filhos = algorithms.varAnd(pop, tb, cxpb=0.6, mutpb=0.3); _corrigir(filhos)
        for ind in filhos: ind.fitness.values = tb.evaluate(ind)
        pop = tb.select(filhos+pop, k=tam_pop); hof.update(pop)
    return np.array(hof[0])

def gerar_para_cultura(chave, cultura):
    global UMIDADE_BASE; UMIDADE_BASE = carregar_previsao()
    alvo = cultura["umidade_alvo"]; melhor = otimizar(alvo)
    u = simular_umidade(melhor); total = float(np.sum(melhor))
    res = {"cultura":chave,"cultura_nome":cultura["nome"],"regiao":"Ribeirao Preto - SP",
           "horizonte_horas":HORAS,"umidade_critica":cultura["umidade_critica"],
           "umidade_alvo":alvo,"total_agua_mm":round(total,2),
           "cronograma_mm_por_hora":[round(float(x),2) for x in melhor],
           "umidade_prevista_sem_irrigacao":[round(float(x),4) for x in UMIDADE_BASE],
           "umidade_estimada_com_irrigacao":[round(float(x),4) for x in u]}
    with open(os.path.join(DATA_DIR, "cronograma_"+chave+".json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    horas = np.arange(HORAS)
    fig, ax1 = plt.subplots(figsize=(11,4.5))
    ax1.bar(horas, melhor, alpha=0.4, color="tab:blue", label="Irrigacao (mm)")
    ax1.set_xlabel("Hora (24h)"); ax1.set_ylabel("Irrigacao (mm)", color="tab:blue")
    ax2 = ax1.twinx()
    ax2.plot(horas, UMIDADE_BASE, "r--", label="Sem irrigacao (LSTM)")
    ax2.plot(horas, u, "g-", linewidth=2, label="Com irrigacao (AG)")
    ax2.axhline(alvo, color="gray", linestyle=":", label="Alvo "+str(alvo))
    ax2.set_ylabel("Umidade (m3/m3)")
    l1,r1 = ax1.get_legend_handles_labels(); l2,r2 = ax2.get_legend_handles_labels()
    ax1.legend(l1+l2, r1+r2, loc="upper center", ncol=2, fontsize=8)
    plt.title("AgroSentinela - Irrigacao otimizada - "+cultura["nome"]); plt.tight_layout()
    os.makedirs(ASSETS_DIR, exist_ok=True)
    plt.savefig(os.path.join(ASSETS_DIR, "grafico_irrigacao_"+chave+".png"), dpi=120); plt.close()
    return total

def main():
    culturas = carregar_culturas()
    alvo = sys.argv[1] if len(sys.argv) > 1 else None
    if alvo and alvo in culturas: culturas = {alvo: culturas[alvo]}
    print("[INFO] Gerando cronogramas por cultura...")
    for ch, c in culturas.items():
        print("  - " + c["nome"].ljust(26) + " -> " + format(gerar_para_cultura(ch, c), ".2f") + " mm/24h")
    print("[OK] cronogramas em data/cronograma_<cultura>.json")

if __name__ == "__main__":
    main()
