from langchain_community.vectorstores import Chroma
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
    """Crea una base vectorial local en formato Chroma (compatible con Render)."""
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documentos = [Document(page_content=chunk) for chunk in splitter.split_text(texto_manual)]
    embeddings = obtener_embeddings()

    persist_dir = f"vectores/{nombre_modelo}"
    os.makedirs(persist_dir, exist_ok=True)

    vectores = Chroma.from_documents(
        documentos,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    vectores.persist()  # guarda físicamente los embeddings
    return vectores


def cargar_vectorstore(nombre_modelo: str):
    """Carga una base vectorial persistente (Chroma)."""
    embeddings = obtener_embeddings()
    persist_dir = f"vectores/{nombre_modelo}"

    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
