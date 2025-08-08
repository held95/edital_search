# 📄 Analisador de Palavras-chave em Documentos

Este é um sistema em **Streamlit** que permite fazer o upload de documentos (PDF, Word ou imagens JPEG) e extrair automaticamente **ocorrências de palavras-chave** com seus respectivos contextos.

---

## 🚀 Funcionalidades

- ✅ Upload de múltiplos arquivos PDF, DOCX e imagens (JPEG/JPG)
- 🔍 Extração de texto e análise de palavras-chave específicas
- 📌 Exibição de até 3 contextos para cada palavra-chave encontrada
- ⏳ Spinner (roda de carregamento) durante o processamento
- 💾 Exportação do relatório final como **PDF** ou **Word (.docx)**

---

## 📦 Requisitos

Instale as dependências com:

```bash
pip install -r requirements.txt
```

> **Importante:**  
> Para a conversão de PDFs com imagem (OCR), é necessário instalar o [poppler](https://github.com/Belval/pdf2image#installing-poppler).  
> No Linux: `sudo apt install poppler-utils`  
> No Windows: baixe e configure o caminho no sistema.

---

## ▶️ Como executar

Rode o app com o comando abaixo:

```bash
streamlit run app.py
```

---

## 📝 Exemplo de uso

1. Clique em **Upload de documentos**
2. Selecione seus arquivos `.pdf`, `.docx`, `.jpg` ou `.jpeg`
3. Clique em **Gerar Relatório**
4. Veja os resultados direto na tela
5. Exporte como **PDF** ou **Word** clicando em **Gerar Arquivo**

---

## 🧠 Palavras-chave buscadas

- Esclarecimento
- Impugnação
- data de abertura
- recursos
- prazo
- horas
- garantia
- caução
- seguro-garantia
- entrega
- atestado de capacidade técnica
- regional
- local

---

## 💻 Hospedagem

Você pode hospedar este projeto gratuitamente usando o [Streamlit Cloud](https://streamlit.io/cloud).  
Basta fazer o upload dos arquivos no GitHub e conectar seu repositório.

---

Feito com ❤️ por Hélder
