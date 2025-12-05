import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector


def main():
    load_dotenv()
    CONNECTION_STRING = os.getenv("DATABASE_URL")
    COLLECTION_NAME = "risk_analysis_docs"

    if not CONNECTION_STRING:
        raise ValueError("DATABASE_URL não encontrada no .env")

    pdf_path = "./docs/"

    print(f"Carregando PDFs da pasta '{pdf_path}'...")
    loader = PyPDFDirectoryLoader(pdf_path)
    documents = loader.load()

    if not documents:
        print("Nenhum PDF encontrado! Verifique a pasta.")

        exit()

    print(f"Carregados {len(documents)} documentos.")

    print("Dividindo os textos em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    print(f"Documentos divididos em {len(chunks)} chunks.")

    print("Gerando embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("Armazenando chunks e embeddings no Neon/PGVector...")
    db = PGVector.from_documents(
        embedding=embeddings,
        documents=chunks,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        pre_delete_collection=True,  # <- ser igual a True garante que começa do zero
    )

    print(f"{len(chunks)} chunks armazenados na coleção '{COLLECTION_NAME}' no Neon.")

    print(db)


if __name__ == "__main__":
    main()
