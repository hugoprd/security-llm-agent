#!/bin/bash

PROVIDER=${LLM_PROVIDER:-ollama}

echo "--- Iniciando Container no modo: $PROVIDER ---"

if [ "$PROVIDER" = "ollama" ]; then
    echo "Iniciando servidor Ollama local..."
    ollama serve &
    sleep 5
else
    echo "Modo Gemini detectado. O servidor Ollama NÃO será iniciado para economizar memória."
fi

cd scripts/llm_main

echo "Iniciando a API FastAPI..."

uvicorn risk_analysis_agent:app --host 0.0.0.0 --port 7860