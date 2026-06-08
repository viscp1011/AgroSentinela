@echo off
cd /d "%~dp0.."
echo Abrindo o painel do AgroSentinela...
start "" "%cd%\src\frontend\index.html"
