import os
from langchain_google_genai import ChatGoogleGenerativeAI, HarmBlockThreshold, HarmCategory


def get_gemini_llm(temperature: float = 0.3):
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "ERRO CRÍTICO: Para usar o Gemini, você precisa configurar a GOOGLE_API_KEY no arquivo .env"
        )

    print("--- Inicializando Conexão com Google Gemini ---")

    return ChatGoogleGenerativeAI(
        model="gemini-pro",  # "gemini-1.5-flash",
        google_api_key=api_key,
        temperature=temperature,
        convert_system_message_to_human=True,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )
