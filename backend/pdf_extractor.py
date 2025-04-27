import pdfplumber
import re
import unicodedata
from typing import Dict, Any, Optional

class PDFExtractor:
    """
    Classe responsável pela extração de dados de exames de sangue de arquivos PDF.
    """
    
    def __init__(self):
        # Padrões de expressão regular para extração de dados
        self.date_pattern = r"DATA COLETA/RECEBIMENTO:\s*(\d{2}/\d{2}/\d{4})"
        self.exam_pattern = r"([A-Za-zÀ-ÖØ-öø-ÿ\s\-]+)\s+(\d+[,.]?\d*)\s*(mg/dL|g/dL|U/L|%|ng/mL|pg|mcg/dL|mEq/L|mmol/L|10\^3/mm3|10\^6/mm3|fL)"
        self.alt_pattern = r"([A-Za-zÀ-ÖØ-öø-ÿ\s\-]+)\s+(\d+[,.]?\d*)\s*$"
        
    def extract_from_pdf(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Extrai dados de um arquivo PDF de exame de sangue.
        
        Args:
            file_path: Caminho para o arquivo PDF
            
        Returns:
            Dicionário com data de coleta e exames extraídos, ou None em caso de erro
        """
        try:
            with pdfplumber.open(file_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"
                
                # Extrair data de coleta
                collection_date = self._extract_collection_date(full_text)
                
                # Extrair exames e valores
                exams = self._extract_exams_and_values(full_text)
                
                return {
                    "data_coleta": collection_date,
                    "exames": exams
                }
        except Exception as e:
            print(f"Erro ao processar PDF: {e}")
            return None
    
    def _extract_collection_date(self, text: str) -> Optional[str]:
        """
        Extrai a data de coleta do texto do PDF.
        
        Args:
            text: Texto extraído do PDF
            
        Returns:
            Data de coleta no formato DD/MM/AAAA ou None se não encontrada
        """
        match = re.search(self.date_pattern, text)
        if match:
            return match.group(1)
        return None
    
    def _extract_exams_and_values(self, text: str) -> Dict[str, float]:
        """
        Extrai os exames e seus valores do texto do PDF.
        
        Args:
            text: Texto extraído do PDF
            
        Returns:
            Dicionário com nomes de exames normalizados e seus valores
        """
        exams = {}
        
        # Procurar por todos os padrões no texto
        for match in re.finditer(self.exam_pattern, text):
            exam_name = match.group(1).strip()
            value = match.group(2).replace(',', '.')
            exams[self._normalize_exam_name(exam_name)] = float(value)
        
        # Procurar pelo padrão alternativo
        for match in re.finditer(self.alt_pattern, text):
            exam_name = match.group(1).strip()
            value = match.group(2).replace(',', '.')
            # Verificar se o nome do exame não é apenas um número ou texto genérico
            if len(exam_name) > 3 and not exam_name.isdigit():
                exams[self._normalize_exam_name(exam_name)] = float(value)
        
        return exams
    
    def _normalize_exam_name(self, name: str) -> str:
        """
        Normaliza o nome do exame conforme especificação.
        
        Args:
            name: Nome original do exame
            
        Returns:
            Nome normalizado (sem acento, minúsculo, sem espaços duplicados)
        """
        # Remover acentos
        name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
        
        # Converter para minúsculo
        name = name.lower()
        
        # Remover espaços duplicados
        name = re.sub(r'\s+', ' ', name).strip()
        
        return name
