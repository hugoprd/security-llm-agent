#!/bin/bash

ollama serve &

sleep 5

echo "Baixando o modelo deepseek-llm (deepseek-r1:1.5b)..."
ollama pull deepseek-r1:1.5b

echo "Iniciando a API FastAPI com Uvicorn"
uvicorn llm_main.ollama_cloud_manager:app --host 0.0.0.0 --port 7860