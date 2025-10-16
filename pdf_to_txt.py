import fitz  # PyMuPDF
import os

def convertir_pdf_a_txt(pdf_path, txt_path):
    doc = fitz.open(pdf_path)
    texto = ""
    for page in doc:
        texto += page.get_text()
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"✅ Convertido: {pdf_path} → {txt_path}")

manuales = {
    "FT125": "manuales/WEB+FT125.pdf",
    "FT150": "manuales/FT150.pdf"
}

os.makedirs("manuales_txt", exist_ok=True)

for modelo, ruta_pdf in manuales.items():
    ruta_txt = f"manuales_txt/{modelo.lower()}.txt"
    convertir_pdf_a_txt(ruta_pdf, ruta_txt)
