from fastapi import FastAPI, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_postgres import PGVector, PGVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.runnables import Runnable

load_dotenv()

app = FastAPI(title="Agente Analista de Risco")


class OllamaAgent:
    def __init__(self):
        self._OLLAMA_BASE_URL = self._get_ollama_url()
        self._CONNECTION_STRING = self._get_connection_string()

        self._text_data = self._get_text_data()
        self._text_splitter = self._get_text_splitter()
        self._docs = self._get_docs()
        self._embedding_model = self._get_embedding_model()
        self._collection_name = self._get_collection_name()
        self._db = self._get_db()
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

    def _get_text_data(self) -> list[str]:
        text_data = [
            "Risco de Injeção de SQL (SQL Injection): Ocorre quando um "
            "atacante insere um código SQL malicioso em uma entrada de dados. "
            "Mitigação: Use Prepared Statements (consultas parametrizadas) e "
            "ORMs. Valide e sanitize todas as entradas do usuário "
            "rigorosamente.",
            "Risco de Cross-Site Scripting (XSS): Acontece quando um script "
            "malicioso é injetado em um site confiável. Mitigação: Valide e "
            "escape todas as entradas de usuário antes de exibi-las no HTML. "
            "Use Content Security Policy (CSP) para restringir a execução de "
            "scripts.",
        ]

        return text_data

    def _get_text_splitter(self) -> RecursiveCharacterTextSplitter:
        return RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    def _get_docs(self) -> Document:
        return self._text_splitter.create_documents(self._text_data)

    def _get_embedding_model(self) -> HuggingFaceEmbeddings:
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def _get_collection_name(self) -> str:
        return "risk_analysis_docs"

    def _get_db(self) -> PGVector:
        pgvector = PGVector.from_documents(
            embedding=self._embedding_model,
            documents=self._docs,
            collection_name=self._collection_name,
            connection=self._CONNECTION_STRING,
            pre_delete_collection=True,
            engine_args={"pool_recycle": 300},  # coloca um tempo de "ociosidade" de 300ms (5min)
        )

        return pgvector

    def _get_retriever(self) -> PGVectorStore:
        return self._db.as_retriever()

    def _get_llm_model(self) -> Ollama:
        return Ollama(base_url=self._OLLAMA_BASE_URL, model="deepseek-llm")

    def _get_template(self) -> str:
        template = """Você é um especialista em análise de riscos de cibersegurança. Com base no
            CONTEXTO abaixo e na ATIVIDADE descrita, identifique o principal risco e sugira uma
            mitigação.

            CONTEXTO: {context}
            ATIVIDADE: "{question}"
            RESPOSTA:
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


if __name__ == "__main__":
    print("--- INICIANDO SERVIDOR FASTAPI ---")
    print("O Agente LLM está pronto para receber pedidos em http://127.0.0.1:8000")

    uvicorn.run(app, host="127.0.0.1", port=8000)
