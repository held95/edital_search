import streamlit as st
import re
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes
import docx
from io import BytesIO

# Palavras-chave
PALAVRAS_CHAVE = [
    "Esclarecimento", "Impugnação", "data de abertura", "recursos",
    "prazo", "horas", "garantia", "caução", "seguro-garantia",
    "entrega", "atestado de capacidade técnica", "regional", "local"
]

def encontrar_contexto(texto, palavra, n_caracteres=120):
    trechos = []
    for match in re.finditer(re.escape(palavra), texto, flags=re.IGNORECASE):
        start = max(match.start() - n_caracteres, 0)
        end = min(match.end() + n_caracteres, len(texto))
        contexto = texto[start:end].replace('\n', ' ').strip()
        trechos.append(contexto)
    return trechos

st.title("🔍 Analisador de Palavras-chave em Documentos")
st.markdown("Faça upload de arquivos PDF, Word ou imagens e clique em **Gerar Relatório**.")

uploaded_files = st.file_uploader(
    "📁 Upload de documentos",
    type=["pdf", "jpg", "jpeg", "png", "docx"],
    accept_multiple_files=True
)

# Inicializa estado
if "relatorios" not in st.session_state:
    st.session_state["relatorios"] = []

# Ao gerar relatório: processa arquivos e salva em session_state
if st.button("🚀 Gerar Relatório") and uploaded_files:
    with st.spinner("🔄 Processando arquivos..."):
        relatorios = []
        for file in uploaded_files:
            st.markdown("---")
            texto = ""
            try:
                ext = file.name.lower().split(".")[-1]

                # PDF
                if ext == "pdf":
                    file.seek(0)
                    leitor = PdfReader(file)
                    for pagina in leitor.pages:
                        texto_pagina = pagina.extract_text()
                        if texto_pagina:
                            texto += texto_pagina
                    # se não extraiu texto, tenta OCR nas páginas como imagem
                    if not texto.strip():
                        file.seek(0)
                        imagens = convert_from_bytes(file.read())
                        for img in imagens:
                            texto += pytesseract.image_to_string(img, lang='por+eng') + '\n'

                # Imagem
                elif ext in ["jpg", "jpeg", "png"]:
                    imagem = Image.open(file)
                    texto = pytesseract.image_to_string(imagem, lang='por+eng')

                # Word
                elif ext == "docx":
                    doc = docx.Document(file)
                    texto = '\n'.join([p.text for p in doc.paragraphs])

                texto_limpo = texto.strip()
                resumo = texto_limpo[:500] + '...' if len(texto_limpo) > 500 else texto_limpo

                # Mostrar prévia na app
                st.subheader(f"📄 Arquivo: {file.name}")
                st.markdown("🔍 **Prévia do Texto:**")
                st.code(resumo)

                # Montar texto que irá pro relatorio final (TXT)
                relatorio_text = [f"📄 Arquivo: {file.name}\n", f"🔍 Prévia do Texto:\n{resumo}\n"]

                for palavra in PALAVRAS_CHAVE:
                    trechos = encontrar_contexto(texto_limpo, palavra)
                    if trechos:
                        st.markdown(f"➡️ **Palavra:** `{palavra}` | Ocorrências: `{len(trechos)}`")
                        relatorio_text.append(f"➡️ Palavra: '{palavra}' | Ocorrências: {len(trechos)}\n")
                        for i, trecho in enumerate(trechos[:3], 1):
                            st.markdown(f"- ✏️ **Contexto {i}:** ...{trecho}...")
                            relatorio_text.append(f"   ✏️ Contexto {i}: ...{trecho}...\n")

                relatorios.append("\n".join(relatorio_text))

            except Exception as e:
                st.error(f"Erro ao processar {file.name}: {e}")

        # salva resultado na sessão (permanece após reruns)
        st.session_state["relatorios"] = relatorios

# Se houver relatórios no estado, mostra botão de download (único botão solicitado)
if st.session_state.get("relatorios"):
    conteudo_txt = "\n------------------------------------------------\n".join(st.session_state["relatorios"])
    # Gera o botão que já faz o download do .txt (um clique)
    st.download_button(
        label="💾 Gerar TXT",
        data=conteudo_txt.encode("utf-8"),
        file_name="relatorio_final.txt",
        mime="text/plain",
        key="download_txt"
    )

    # opcional: botão para limpar o relatório salvo
    if st.button("🗑️ Limpar relatório"):
        st.session_state["relatorios"] = []
        st.experimental_rerun()
