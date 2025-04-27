from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import shutil
from typing import List
import tempfile

from pdf_extractor import PDFExtractor
from excel_generator import ExcelGenerator

app = FastAPI(title="API de Processamento de Exames de Sangue")

# Configuração de CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar a origem exata
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretório para armazenar arquivos temporários
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(TEMP_DIR, exist_ok=True)

# Inicializar extrator de PDF e gerador de Excel
pdf_extractor = PDFExtractor()
excel_generator = ExcelGenerator(TEMP_DIR)

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Endpoint para upload de arquivos PDF de exames de sangue.
    Processa os PDFs, extrai os dados e gera uma planilha Excel.
    
    Args:
        files: Lista de arquivos PDF enviados pelo cliente
        
    Returns:
        Arquivo Excel com os dados extraídos
    """
    if not files:
        raise HTTPException(status_code=400, detail="Nenhum arquivo enviado")
    
    processed_data = []
    
    for file in files:
        # Verificar se é um PDF
        if not file.filename.lower().endswith('.pdf'):
            continue
        
        # Salvar o arquivo temporariamente
        temp_file = os.path.join(TEMP_DIR, file.filename)
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Processar o PDF
        result = pdf_extractor.extract_from_pdf(temp_file)
        if result and result["data_coleta"]:
            processed_data.append(result)
        
        # Remover o arquivo temporário
        os.remove(temp_file)
    
    if not processed_data:
        raise HTTPException(status_code=400, detail="Nenhum dado válido extraído dos PDFs")
    
    # Gerar planilha Excel
    excel_path = excel_generator.generate_excel(processed_data)
    
    # Retornar o arquivo Excel
    return FileResponse(
        path=excel_path, 
        filename="exames.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.get("/")
async def root():
    """
    Endpoint raiz para verificar se a API está funcionando.
    
    Returns:
        Mensagem de status da API
    """
    return {"message": "API de Processamento de Exames de Sangue"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
