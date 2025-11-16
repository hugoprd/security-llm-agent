#!/bin/bash

ollama serve &

sleep 3

echo "Iniciando a API FastAPI com Uvicorn..."
uvicorn llm_main.ollama_cloud_manager:app --host 0.0.0.0 --port 7860