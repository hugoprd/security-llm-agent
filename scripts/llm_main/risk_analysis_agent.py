from fastapi import FastAPI, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_postgres import PGVector, PGVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

try:
    from gemini_provider import get_gemini_llm
    from ollama_provider import get_ollama_llm
except ImportError as e:
    print(
        "ERRO CRÍTICO: Faltam os arquivos de provedor (gemini_provider.py ou ollama_provider.py).",
        f"Erro: {e}",
    )
    exit(1)

load_dotenv()

app = FastAPI(title="Agente Analista de Risco (Modular)")


class RiskAnalysisAgent:
    def __init__(self):
        self._CONNECTION_STRING = self._get_connection_string()
        self._collection_name = "risk_analysis_docs"
        self._embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self._retriever = self._setup_retriever()
        self.provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        print(f"--- MODO SELECIONADO: {self.provider.upper()} ---")
        self._llm_model = self._select_llm_provider()
        self._rag_chain = self._build_rag_chain()

    def _get_connection_string(self):
        conn = os.getenv("DATABASE_URL")
        if not conn:
            raise ValueError("ERRO: A DATABASE_URL não foi configurada no arquivo .env")
        return conn

    def _setup_retriever(self) -> PGVectorStore:
        db_connection = PGVector(
            collection_name=self._collection_name,
            connection=self._CONNECTION_STRING,
            embeddings=self._embedding_model,
            engine_args={"pool_recycle": 300},
        )
        return db_connection.as_retriever(search_kwargs={"k": 3})

    def _select_llm_provider(self):
        if self.provider == "gemini":
            return get_gemini_llm(temperature=0.3)
        elif self.provider == "ollama":
            return get_ollama_llm(model_name="qwen2.5:3b", temperature=0.3)
        else:
            raise ValueError(
                f"Provedor '{self.provider}' desconhecido. ",
                "Configure LLM_PROVIDER como 'gemini' ou 'ollama' no .env.",
            )

    def _build_rag_chain(self) -> Runnable:
        template = """
            Você é um auditor de segurança de aplicações experiente (OWASP).
            Sua tarefa é analisar a 'ATIVIDADE DO SISTEMA' descrita abaixo e identificar falhas de segurança baseando-se no 'CONTEXTO TÉCNICO' fornecido.

            CONTEXTO TÉCNICO (Base de Conhecimento):
            {context}

            ATIVIDADE DO SISTEMA (O que está acontecendo):
            "{question}"

            INSTRUÇÕES:
            1. Verifique violações de autenticação, autorização ou controle de acesso.
            2. Se a atividade menciona "sem autenticação", verifique riscos de Acesso Não Autorizado.
            3. Não invente riscos (XSS/SQLi) se não forem pertinentes à descrição.

            FORMATO DA RESPOSTA (Markdown):
            **Risco Identificado:** [Nome do Risco]
            **Análise:** [Explicação breve do porquê é um risco]
            **Recomendação:** [Ação prática para corrigir]

            Se o contexto for insuficiente, responda apenas: "Não foi possível identificar o risco com base nos documentos fornecidos."
        """
        prompt = PromptTemplate.from_template(template)

        rag_chain = (
            {"context": self._retriever, "question": RunnablePassthrough()}
            | prompt
            | self._llm_model
            | StrOutputParser()
        )
        return rag_chain


try:
    agent = RiskAnalysisAgent()
except Exception as e:
    print(f"FATAL: Falha ao iniciar o agente: {e}")
    agent = None


class ActivityRequest(BaseModel):
    description: str


@app.get("/")
def read_root():
    if not agent:
        return {"Status": "Erro na inicialização", "Detalhe": "Verifique os logs do terminal"}

    return {
        "Status": "Online",
        "Provedor Ativo": agent.provider.upper(),
        "Modelo": "Gemini 1.5 Flash" if agent.provider == "gemini" else "Ollama Local",
    }


@app.post("/generate-suggestion")
def generate_suggestion(activity: ActivityRequest):
    if not agent:
        raise HTTPException(status_code=500, detail="O agente não foi inicializado corretamente.")

    try:
        print(f"--> Processando pedido via {agent.provider}...")
        suggestion = agent._rag_chain.invoke(activity.description)
        return {"suggestion": suggestion}
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro no processamento ({agent.provider}): {str(e)}"
        )


@app.post("/warmup")
def warmup_agent():
    if not agent:
        raise HTTPException(status_code=500, detail="Agente não inicializado.")
    try:
        agent._llm_model.invoke("Hi")
        return {"status": "Warmup complete", "provider": agent.provider}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Warmup failed: {e}")


if __name__ == "__main__":
    print("--- INICIANDO SERVIDOR AGENTE IA ---")
    uvicorn.run(app, host="127.0.0.1", port=8000)
