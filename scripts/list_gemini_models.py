import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("ERRO: A variável GOOGLE_API_KEY não foi encontrada no arquivo .env")

    exit(1)

genai.configure(api_key=api_key)

print(f"--- Consultando modelos disponíveis para a chave: {api_key[:5]}... ---")

try:
    models = genai.list_models()

    found_any = False
    for m in models:
        if "generateContent" in m.supported_generation_methods:
            found_any = True
            print(f"X---> Nome Técnico: {m.name}")
            print(f"   Nome Visual: {m.display_name}")
            print(f"   Versão: {m.version}")
            print("-" * 30)

    if not found_any:
        print(
            "Nenhum modelo de geração de texto encontrado. Verifique se sua API Key tem permissões corretas."
        )

except Exception as e:
    print(f"Erro ao conectar na API do Google: {e}")
