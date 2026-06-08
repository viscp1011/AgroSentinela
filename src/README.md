# src/ — Código-fonte do AgroSentinela
- **backend/**: `coleta_dados.py` (Open-Meteo), `modelo_lstm.py` (IA 1 - LSTM),
  `algoritmo_genetico.py` (IA 2 - DEAP), `main.py` (API FastAPI multi-ESP32).
- **frontend/**: painel `index.html` + `style.css` + `app.js` (Chart.js).
- **esp32/**: `esp32.ino` (4 sensores, POO) + `diagram.json` (Wokwi) + `enviar_leitura_teste.py`.
- **voz/**: `assistente_voz.py` (TTS/STT).
- **infra/**: AWS serverless simulada (CloudFormation + Lambda).
