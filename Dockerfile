# Dockerfile para o sistema de processamento de exames de sangue
# Baseado em Python para o backend e com suporte para o frontend React

# Estágio de build para o frontend
FROM node:20 AS frontend-build

WORKDIR /app/frontend

# Copiar apenas o package.json primeiro
COPY frontend/package.json ./

# Instalar dependências
RUN npm install

# Copiar código fonte do frontend
COPY frontend/ ./

# Construir o frontend
RUN npm run build

# Imagem principal para o backend
FROM python:3.10-slim

WORKDIR /app

# Instalar dependências do sistema necessárias para pdfplumber e outras bibliotecas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt e instalar dependências Python
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do backend diretamente para o diretório raiz
COPY backend/*.py ./

# Criar diretório para dados
RUN mkdir -p data

# Criar diretório para o frontend
RUN mkdir -p frontend/dist

# Copiar o frontend construído
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Criar um arquivo main.py modificado para servir o frontend
RUN echo 'from fastapi import FastAPI, File, UploadFile, HTTPException\n\
from fastapi.responses import FileResponse\n\
from fastapi.middleware.cors import CORSMiddleware\n\
from fastapi.staticfiles import StaticFiles\n\
import uvicorn\n\
import os\n\
import shutil\n\
from typing import List\n\
\n\
from pdf_extractor import PDFExtractor\n\
from excel_generator import ExcelGenerator\n\
\n\
app = FastAPI(title="API de Processamento de Exames de Sangue")\n\
\n\
# Configuração de CORS para permitir requisições do frontend\n\
app.add_middleware(\n\
    CORSMiddleware,\n\
    allow_origins=["*"],\n\
    allow_credentials=True,\n\
    allow_methods=["*"],\n\
    allow_headers=["*"],\n\
)\n\
\n\
# Diretório para armazenar arquivos temporários\n\
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")\n\
os.makedirs(TEMP_DIR, exist_ok=True)\n\
\n\
# Inicializar extrator de PDF e gerador de Excel\n\
pdf_extractor = PDFExtractor()\n\
excel_generator = ExcelGenerator(TEMP_DIR)\n\
\n\
@app.post("/upload")\n\
async def upload_files(files: List[UploadFile] = File(...)):\n\
    if not files:\n\
        raise HTTPException(status_code=400, detail="Nenhum arquivo enviado")\n\
    \n\
    processed_data = []\n\
    \n\
    for file in files:\n\
        # Verificar se é um PDF\n\
        if not file.filename.lower().endswith(".pdf"):\n\
            continue\n\
        \n\
        # Salvar o arquivo temporariamente\n\
        temp_file = os.path.join(TEMP_DIR, file.filename)\n\
        with open(temp_file, "wb") as buffer:\n\
            shutil.copyfileobj(file.file, buffer)\n\
        \n\
        # Processar o PDF\n\
        result = pdf_extractor.extract_from_pdf(temp_file)\n\
        if result and result["data_coleta"]:\n\
            processed_data.append(result)\n\
        \n\
        # Remover o arquivo temporário\n\
        os.remove(temp_file)\n\
    \n\
    if not processed_data:\n\
        raise HTTPException(status_code=400, detail="Nenhum dado válido extraído dos PDFs")\n\
    \n\
    # Gerar planilha Excel\n\
    excel_path = excel_generator.generate_excel(processed_data)\n\
    \n\
    # Retornar o arquivo Excel\n\
    return FileResponse(\n\
        path=excel_path, \n\
        filename="exames.xlsx",\n\
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"\n\
    )\n\
\n\
@app.get("/")\n\
async def root():\n\
    return {"message": "API de Processamento de Exames de Sangue"}\n\
\n\
# Montar arquivos estáticos do frontend\n\
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend/dist")\n\
if os.path.exists(frontend_dir):\n\
    app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")\n\
\n\
if __name__ == "__main__":\n\
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)' > main.py

# Configurar variáveis de ambiente
ENV PORT=8000

# Expor a porta
EXPOSE ${PORT}

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
