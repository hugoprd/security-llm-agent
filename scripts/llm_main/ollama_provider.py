from langchain_ollama import OllamaLLM


def get_ollama_llm(
    base_url: str = "http://127.0.0.1:11434",
    model_name: str = "qwen2.5:3b",
    temperature: float = 0.3,
):
    print(f"--- Inicializando Conexão com Ollama Local ({model_name}) ---")

    return OllamaLLM(
        base_url=base_url,
        model=model_name,
        temperature=temperature,
        timeout=300.0,  # 5 minutos de timeout para evitar desconexões
    )
