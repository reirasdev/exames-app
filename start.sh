#!/bin/sh
# Iniciar o backend em segundo plano
cd /app && uvicorn main:app --host 0.0.0.0 --port 8000 &

# Iniciar o Nginx em primeiro plano
nginx -g 'daemon off;'
