from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def obtener_embeddings():
    provider = os.getenv("EMBEDDING_PROVIDER", "huggingface").lower()

    if provider == "openai":
        print("🔹 Usando embeddings de OpenAI")
        return OpenAIEmbeddings(model="text-embedding-3-small")
    else:
        print("🔹 Usando embeddings de HuggingFace (por defecto)")
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def crear_vectorstore(nombre_modelo: str, texto_manual: str):
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documentos = [Document(page_content=chunk) for chunk in splitter.split_text(texto_manual)]
    embeddings = obtener_embeddings()
    vectores = FAISS.from_documents(documentos, embeddings)

    os.makedirs("vectores", exist_ok=True)
    vectores.save_local(f"vectores/{nombre_modelo}")
    return vectores

def cargar_vectorstore(nombre_modelo: str):
    embeddings = obtener_embeddings()
    return FAISS.load_local(
        f"vectores/{nombre_modelo}",
        embeddings,
        allow_dangerous_deserialization=True
    )
