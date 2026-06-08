@echo off
chcp 65001 >nul
title AgroSentinela - Tunel (cloudflared)
echo Antes: o backend precisa estar rodando (RODAR_AGROSENTINELA.bat).
where cloudflared >nul 2>&1
if errorlevel 1 ( echo Instalando cloudflared... & winget install --id Cloudflare.cloudflared -e --accept-package-agreements --accept-source-agreements )
where cloudflared >nul 2>&1
if errorlevel 1 ( echo [ERRO] Baixe cloudflared: https://github.com/cloudflare/cloudflared/releases & pause & exit /b 1 )
echo Copie a URL https://...trycloudflare.com que aparecer e cole no esp32.ino (URL_BACKEND + /api/leitura).
cloudflared tunnel --url http://localhost:8000
pause
