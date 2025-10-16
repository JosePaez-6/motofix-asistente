from dotenv import load_dotenv
load_dotenv()

from loader import crear_vectorstore

modelos = {
    "FT125": "manuales_txt/ft125.txt",
    "FT150": "manuales_txt/ft150.txt"
}

for modelo, ruta_txt in modelos.items():
    with open(ruta_txt, "r", encoding="utf-8") as f:
        texto = f.read()
    print(f"📦 Procesando: {modelo}")
    crear_vectorstore(modelo, texto)
