
import streamlit as st
import re
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
from collections import defaultdict

# Palavras-chave
PALAVRAS_CHAVE = [
    "Esclarecimento", "Impugnação", "data de abertura", "recursos",
    "prazo", "horas", "garantia", "caução", "seguro-garantia",
    "entrega", "atestado de capacidade técnica", "regional", "local"
]

# Função para encontrar contexto das palavras
def encontrar_contexto(texto, palavra, n_caracteres=120):
    trechos = []
    for match in re.finditer(re.escape(palavra), texto, flags=re.IGNORECASE):
        start = max(match.start() - n_caracteres, 0)
        end = min(match.end() + n_caracteres, len(texto))
        contexto = texto[start:end].replace('\n', ' ').strip()
        trechos.append(contexto)
    return trechos

# Título
st.title("🔍 Analisador de Palavras-chave em Documentos")
st.markdown("Faça upload de arquivos PDF ou imagens e clique em **Gerar Relatório**.")

# Upload
uploaded_files = st.file_uploader("📁 Upload de documentos", type=["pdf", "jpg", "jpeg"], accept_multiple_files=True)

if st.button("🚀 Gerar Relatório") and uploaded_files:
    for file in uploaded_files:
        st.markdown("---")
        texto = ''
        try:
            if file.name.lower().endswith('.pdf'):
                leitor = PdfReader(file)
                for pagina in leitor.pages:
                    texto_pagina = pagina.extract_text()
                    if texto_pagina:
                        texto += texto_pagina

                if not texto.strip():
                    imagens = convert_from_bytes(file.read())
                    for img in imagens:
                        texto += pytesseract.image_to_string(img, lang='por+eng') + '\n'

            elif file.name.lower().endswith(('.jpg', '.jpeg')):
                imagem = Image.open(file)
                texto = pytesseract.image_to_string(imagem, lang='por+eng')

            texto_limpo = texto.strip()
            resumo = texto_limpo[:500] + '...' if texto_limpo else '(Sem texto extraído)'

            st.subheader(f"📄 Arquivo: {file.name}")
            st.markdown("🔍 **Prévia do Texto:**")
            st.code(resumo)

            for palavra in PALAVRAS_CHAVE:
                trechos = encontrar_contexto(texto_limpo, palavra)
                if trechos:
                    st.markdown(f"➡️ **Palavra:** `{palavra}` | Ocorrências: `{len(trechos)}`")
                    for i, trecho in enumerate(trechos[:3], 1):
                        st.markdown(f"- ✏️ **Contexto {i}:** ...{trecho}...")

        except Exception as e:
            st.error(f"Erro ao processar {file.name}: {e}")
