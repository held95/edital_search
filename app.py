import streamlit as st
import re
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
import pytesseract
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configuração do Tesseract (caso necessário, ajuste o caminho)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.title("Leitor de Editais com Busca de Palavras")

# Lista de palavras para busca
palavras_chave = ["Esclarecimento", "Edital", "Licitação"]

uploaded_file = st.file_uploader("Envie o arquivo PDF", type=["pdf"])

if uploaded_file is not None:
    texto_extraido = ""

    # Leitura do PDF
    try:
        pdf = PdfReader(uploaded_file)
        for pagina in pdf.pages:
            texto_extraido += pagina.extract_text() or ""

    except Exception:
        # Caso não consiga ler como texto, tenta via OCR
        imagens = convert_from_bytes(uploaded_file.read())
        for img in imagens:
            texto_extraido += pytesseract.image_to_string(img, lang='por')

    # Limpa e prepara texto
    texto_extraido = re.sub(r'\s+', ' ', texto_extraido).strip()

    # Exibe o conteúdo no terminal e no Streamlit
    st.subheader("Resumo do conteúdo lido:")
    st.write(texto_extraido)

    # Botão único para baixar PDF do que foi lido
    def gerar_pdf(conteudo):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        largura, altura = letter

        y = altura - 40
        for linha in conteudo.split("\n"):
            if y < 40:  # Nova página se chegar ao final
                c.showPage()
                y = altura - 40
            c.drawString(40, y, linha)
            y -= 15

        c.save()
        buffer.seek(0)
        return buffer

    pdf_pronto = gerar_pdf(texto_extraido)

    st.download_button(
        label="📄 Baixar PDF do que foi lido no terminal",
        data=pdf_pronto,
        file_name="relatorio_leitura.pdf",
        mime="application/pdf"
    )
