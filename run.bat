@echo off
cd %~dp0
docker run --rm -v "%cd%\.:/app" -w /app python:3.11-slim python chkwar.py
pause

REM para entrar al bash
::cd /d %~dp0
::docker run -it --name chkwar_test -v "%cd%\compartido:/app" -w /app python:3.11-slim bash