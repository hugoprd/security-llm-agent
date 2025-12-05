import os
from langchain_google_genai import ChatGoogleGenerativeAI


def get_gemini_llm(temperature: float = 0.3):
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "ERRO CRÍTICO: Para usar o Gemini, você precisa configurar a GOOGLE_API_KEY no arquivo .env"
        )

    print("--- Inicializando Conexão com Google Gemini ---")

    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-001",
        google_api_key=api_key,
        temperature=temperature,
    )
