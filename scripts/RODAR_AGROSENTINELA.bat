@echo off
chcp 65001 >nul
title AgroSentinela - Servidor
cd /d "%~dp0.."
set "RAIZ=%cd%"
echo ==================================================
echo   AgroSentinela - iniciando o servidor...
echo ==================================================
python --version >nul 2>&1
if errorlevel 1 (
  echo [AVISO] Python nao encontrado. Abrindo painel em modo demonstracao...
  start "" "%RAIZ%\src\frontend\index.html"
  pause & exit /b 0
)
if not exist ".venv\Scripts\python.exe" ( echo Criando ambiente isolado... & python -m venv .venv )
set "PY=%RAIZ%\.venv\Scripts\python.exe"
"%PY%" -c "import uvicorn, fastapi" 2>nul
if errorlevel 1 ( echo Instalando servidor ^(leve^)... & "%PY%" -m pip install --upgrade pip & "%PY%" -m pip install fastapi uvicorn )
"%PY%" -c "import uvicorn, fastapi" 2>nul
if errorlevel 1 ( echo [AVISO] Sem servidor. Abrindo demonstracao... & start "" "%RAIZ%\src\frontend\index.html" & pause & exit /b 0 )
cd src\backend
echo Abrindo http://localhost:8000/app
start "AgroSentinela API" "%PY%" -m uvicorn main:app --port 8000
timeout /t 6 >nul
start "" http://localhost:8000/app
echo Esta janela pode ser fechada.
pause
