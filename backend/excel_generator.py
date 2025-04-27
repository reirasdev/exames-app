import pandas as pd
import os
from typing import List, Dict, Any

class ExcelGenerator:
    """
    Classe responsável pela geração de planilhas Excel a partir dos dados extraídos dos PDFs.
    """
    
    def __init__(self, output_dir: str):
        """
        Inicializa o gerador de Excel.
        
        Args:
            output_dir: Diretório onde a planilha Excel será salva
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_excel(self, data_list: List[Dict[str, Any]]) -> str:
        """
        Gera uma planilha Excel a partir dos dados extraídos dos PDFs.
        
        Args:
            data_list: Lista de dicionários contendo data de coleta e exames
            
        Returns:
            Caminho para o arquivo Excel gerado
        """
        # Criar um DataFrame vazio
        df = pd.DataFrame()
        
        # Adicionar coluna de data
        dates = [item["data_coleta"] for item in data_list if item["data_coleta"]]
        df["Data da Coleta"] = dates
        
        # Obter todos os tipos de exames únicos
        all_exams = set()
        for item in data_list:
            all_exams.update(item["exames"].keys())
        
        # Adicionar colunas para cada tipo de exame
        for exam in sorted(all_exams):
            df[exam] = None
            
            # Preencher valores para cada data
            for i, item in enumerate(data_list):
                if item["data_coleta"] and exam in item["exames"]:
                    df.loc[i, exam] = item["exames"][exam]
        
        # Ordenar por data
        df["Data da Coleta"] = pd.to_datetime(df["Data da Coleta"], format="%d/%m/%Y")
        df = df.sort_values("Data da Coleta")
        df["Data da Coleta"] = df["Data da Coleta"].dt.strftime("%d/%m/%Y")
        
        # Caminho para salvar o Excel
        excel_path = os.path.join(self.output_dir, "exames.xlsx")
        
        # Salvar como Excel
        df.to_excel(excel_path, index=False)
        
        return excel_path
