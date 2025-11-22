from fastapi import FastAPI, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_postgres import PGVector, PGVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

load_dotenv()

app = FastAPI(title="Agente Analista de Risco")


class OllamaAgent:
    def __init__(self):
        self._OLLAMA_BASE_URL = self._get_ollama_url()
        self._CONNECTION_STRING = self._get_connection_string()

        self._embedding_model = self._get_embedding_model()
        self._collection_name = self._get_collection_name()
        self._retriever = self._get_retriever()
        self._llm_model = self._get_llm_model()
        self._template = self._get_template()
        self._prompt_template = self._get_prompt_template()
        self._rag_chain = self._get_rag_chain()

    def _get_ollama_url(self) -> str:
        return "http://127.0.0.1:11434"

    def _get_connection_string(self):
        CONNECTION_STRING = os.getenv("DATABASE_URL")

        # print(f">>> STRING DA CONEXAO: {CONNECTION_STRING}")

        if not CONNECTION_STRING:
            raise ValueError(
                "A Connection String do banco de dados (DATABASE_URL) não foi "
                "configurada como secret."
            )

        return CONNECTION_STRING

    def _get_embedding_model(self) -> HuggingFaceEmbeddings:
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def _get_collection_name(self) -> str:
        return "risk_analysis_docs"

    def _get_retriever(self) -> PGVectorStore:
        db_connection = PGVector(
            collection_name=self._collection_name,
            connection=self._CONNECTION_STRING,
            embeddings=self._embedding_model,
            engine_args={"pool_recycle": 300},  # timeout de 5min (300ms)
        )

        # tentativa de limitar o kwargs para 3 para não sobrecarregar o modelo pequeno
        return db_connection.as_retriever(search_kwargs={"k": 3})

    def _get_llm_model(self) -> OllamaLLM:
        return OllamaLLM(
            base_url=self._OLLAMA_BASE_URL,
            model="qwen2.5:1.5b",
            temperature=0.3,  # dando menor criatividade para uma resposta mais rápida e direta
            timeout=300.0,  # 300 segundos (5min) de tolerância
        )

    def _get_template(self) -> str:
        template = """
            Atue como analista de cibersegurança sênior.
            Use APENAS o contexto abaixo para responder. Se a resposta não estiver no contexto, diga que não sabe.
            
            CONTEXTO: {context}
            
            TAREFA: Analise a atividade "{question}".
            
            SAÍDA ESPERADA:
            1. Identifique o Risco Principal.
            2. Sugira uma Mitigação técnica.
            Responda em Português do Brasil de forma concisa.
        """

        return template

    def _get_prompt_template(self) -> PromptTemplate:
        return PromptTemplate.from_template(self._template)

    def _get_rag_chain(self) -> Runnable:
        rag_chain = (
            {"context": self._retriever, "question": RunnablePassthrough()}
            | self._prompt_template
            | self._llm_model
            | StrOutputParser()
        )

        return rag_chain


class ActivityRequest(BaseModel):
    description: str


ollama_agent = OllamaAgent()
rag_chain = ollama_agent._rag_chain


@app.get("/")
def read_root():
    return {"Status": "Agente LLM com RAG e PostgreSQL está online"}


@app.post("/generate-suggestion")
def generate_suggestion(activity: ActivityRequest):
    try:
        suggestion = rag_chain.invoke(activity.description)

        return {"suggestion": suggestion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {e}")


@app.post("/warmup")
def warmup_agent():
    model_instance = ollama_agent._llm_model

    try:
        # aqui apenas faz uma requisição simples e rápida para forçar o carregamento do modelo
        model_instance.invoke("Hi")

        return {"status": "Warmup complete", "model": model_instance.model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Warmup failed: {e}")


if __name__ == "__main__":
    print("--- INICIANDO SERVIDOR FASTAPI ---")
    print("O Agente LLM está pronto para receber pedidos em http://127.0.0.1:8000")

    uvicorn.run(app, host="127.0.0.1", port=8000)
