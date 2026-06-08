@echo off
chcp 65001 >nul
title AgroSentinela - Compilar ESP32
cd /d "%~dp0..\src\esp32"
echo ==================================================
echo   Compilar firmware do ESP32 (arduino-cli)
echo   1a vez baixa o core do ESP32 (~centenas de MB).
echo ==================================================
where arduino-cli >nul 2>&1
if errorlevel 1 (
  echo Instalando arduino-cli via winget...
  winget install --id ArduinoSA.CLI -e --accept-package-agreements --accept-source-agreements
  echo Feche e reabra este .bat para o arduino-cli entrar no PATH.
  pause & exit /b 0
)
echo [1/4] Indice de placas...
arduino-cli config init >nul 2>&1
arduino-cli config add board_manager.additional_urls https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
arduino-cli core update-index
echo [2/4] Core esp32 (demorado)...
arduino-cli core install esp32:esp32
echo [3/4] Bibliotecas DHT...
arduino-cli lib install "DHT sensor library"
arduino-cli lib install "Adafruit Unified Sensor"
echo [4/4] Compilando...
arduino-cli compile --fqbn esp32:esp32:esp32 --output-dir build .
if exist "build\esp32.ino.bin" ( echo SUCESSO! Agora no VS Code: F1 -^> Wokwi: Start Simulator ) else ( echo [ERRO] Veja as mensagens acima. )
pause
