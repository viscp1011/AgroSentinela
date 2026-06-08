# 🌱 AgroSentinela

**IA como Fertilizante Digital — um novo agronegócio do amanhã**
Global Solution 2026.1 — FIAP — Fase 7

> Plataforma de **baixo custo** para o pequeno produtor rural que une um sensor
> **ESP32** (simulado), **dados climáticos/de satélite reais** e **Inteligência
> Artificial** para **prever risco hídrico**, **otimizar a irrigação** e
> **alertar o produtor por voz**.

**QUERO CONCORRER** 🏆

---

## 👥 Integrantes

| Nome | RM | E-mail |
|------|----|--------|
| Vitorio Stevanatto Compri Paciulo | (preencher RM) | vitorioscp@gmail.com |

> Grupo 14 — entrega individual autorizada pela professora.

---

## 🛰️ Ponte com a Economia Espacial

A pergunta central da GS é: *“Como a IA e as tecnologias digitais podem
transformar a nova economia espacial e gerar impacto positivo na Terra?”*

O AgroSentinela faz os **dados de sensoriamento descerem até quem planta**:
clima, umidade do solo e NDVI orbital (Embrapa/INPE) viram **decisões práticas
de irrigação** na mão do pequeno produtor. A metáfora-guia é a do *“drone barato
de grande impacto”*: tecnologia simples e barata, com potencial enorme no campo.

---

## 🧩 Arquitetura

![Arquitetura](assets/arquitetura.png)

```
ESP32 simulado (Wokwi) → leituras de campo
   → Backend FastAPI: coleta clima REAL (Open-Meteo) + junta com o sensor
      → LSTM (Keras): prevê umidade do solo / risco hídrico
         → Algoritmo Genético (DEAP): otimiza o cronograma de irrigação (água x custo)
            → AWS serverless SIMULADA (Lambda + SNS + SQS): dispara alertas
               → Assistente de voz (TTS/STT): comunica o produtor
                  → Dashboard (HTML/CSS/JS + Chart.js): exibe tudo
```

---

## 🗺️ Mapeamento Módulo → Disciplina

| Capítulo | Módulo no projeto |
|----------|-------------------|
| 1 — Consolidação de sistema | Integração geral (backend FastAPI) |
| 2 — Redes Neurais Recorrentes | `modelo_lstm.py` (previsão hídrica) |
| 3 — Fala ↔ Texto | `assistente_voz.py` (TTS/STT) |
| 4 — Algoritmos Genéticos | `algoritmo_genetico.py` (DEAP) |
| 5 — AWS assíncrono / alertas | `infra/` Lambda + SNS + SQS |
| 6 — Microsserviços / CloudFormation | `infra/template.yaml` |
| 7 — IA como serviço / cognitivo | assistente de voz cognitivo |
| 8 — POO com ESP32 | `src/esp32/sketch.ino` |
| 9 — Red Team vs Blue Team | `docs/seguranca.md` |

---

## 📊 Fonte de Dados (real e gratuita)

- **Open-Meteo Historical Weather API** — sem cadastro, sem chave, uso livre.
- Variáveis: temperatura do ar, umidade relativa, precipitação,
  evapotranspiração de referência (ET₀), temperatura do solo, umidade do solo
  (0–7 cm e 7–28 cm).
- Região monitorada (escolha do autor): **Ribeirão Preto / SP**
  (lat **-21.17**, lon **-47.81**) — polo sucroenergético e de grãos.
- Complemento citado: **NDVI** de fontes públicas (Embrapa/INPE).

---

## 🚀 Como rodar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Coletar os dados climáticos reais
```bash
cd src/backend
python coleta_dados.py            # gera data/dados_climaticos.csv
```

### 3. Treinar o LSTM e gerar a previsão
```bash
python modelo_lstm.py             # gera modelo, previsao.json e gráfico
```

### 4. Otimizar o cronograma de irrigação
```bash
python algoritmo_genetico.py      # gera cronograma_irrigacao.json e gráfico
```

### 5. Subir o backend (API + dashboard)
```bash
uvicorn main:app --reload --port 8000
# Dashboard:  http://localhost:8000/app
# API:        http://localhost:8000/api/dashboard
```

### 6. Assistente de voz
```bash
cd ../voz
python assistente_voz.py          # gera assets/alerta_voz.mp3
```

### 7. ESP32 no Wokwi
Importe `src/esp32/` em https://wokwi.com (sketch.ino + diagram.json).
Ajuste `URL_BACKEND` para o IP da sua máquina e rode a simulação.

---

## 📁 Estrutura do repositório

```
GLOBAL-SOLUTION-AGROSENTINELA/
├── README.md
├── requirements.txt
├── assets/            # diagramas, gráficos, áudio do alerta
├── data/              # CSV coletado + saídas dos modelos (gerados)
├── docs/              # seção de segurança (Red/Blue) e rascunhos do PDF
├── infra/             # template CloudFormation + código da Lambda (simulado)
└── src/
    ├── backend/       # coleta_dados.py, modelo_lstm.py, algoritmo_genetico.py, main.py
    ├── frontend/      # index.html, style.css, app.js (Chart.js)
    ├── esp32/         # sketch.ino, diagram.json (Wokwi)
    └── voz/           # assistente_voz.py
```

---

## 🧪 Resultados obtidos (dados reais)

- **17.496** registros horários reais coletados (2 anos, Ribeirão Preto/SP).
- LSTM com **MAE ≈ 0.010 m³/m³** na previsão de umidade do solo.
- Algoritmo Genético: mantém a umidade no alvo (0.22 m³/m³) usando apenas
  **~8 mm** de água nas 24h, contra ~96 mm de uma irrigação fixa ingênua.

---

## 🌾 Irrigação por cultura

Cada cultura tem necessidade hídrica diferente. O sistema usa limiares próprios
(em `data/culturas.json`) e o algoritmo genético gera um cronograma específico:

| Cultura | Umid. crítica | Umid. alvo | Água 24h |
|---------|---------------|------------|----------|
| Cana-de-açúcar | 0,18 | 0,24 | 11,3 mm |
| Soja | 0,20 | 0,26 | 14,7 mm |
| Milho | 0,20 | 0,27 | 16,2 mm |
| Café | 0,22 | 0,28 | 17,8 mm |
| Citros (laranja) | 0,20 | 0,26 | 14,7 mm |
| Hortaliças | 0,25 | 0,32 | 24,0 mm |

No dashboard, troque a cultura no seletor do topo — gráficos, risco e água mudam.
A condição climática **atual** (tempo real) é puxada da Open-Meteo forecast API.

## 🔌 ESP32 / Wokwi end-to-end

Passo a passo completo em **`docs/wokwi_guia.md`** (extensão do VS Code, ngrok ou
o script `src/esp32/enviar_leitura_teste.py` para ver o painel reagir).

## 🔗 Links

- Repositório: https://github.com/viscp1011/AgroSentinela
- Vídeo (YouTube, não listado): *(colar link)*

## 📜 Licença
Projeto acadêmico — FIAP Global Solution 2026.1.
