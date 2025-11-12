#!/bin/bash

ollama serve &

sleep 5

echo "Baixando o modelo deepseek-llm..."
ollama pull deepseek-llm

echo "Iniciando a API FastAPI com Uvicorn"
uvicorn llm_main.ollama_cloud_manager:app --host 0.0.0.0 --port 7860