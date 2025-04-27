# API de Processamento de Exames de Sangue

Esta documentação descreve a API do sistema de processamento de exames de sangue em PDF.

## Endpoints

### `GET /`

Endpoint para verificar se a API está funcionando.

**Resposta:**
```json
{
  "message": "API de Processamento de Exames de Sangue"
}
```

### `POST /upload`

Endpoint para upload de arquivos PDF de exames de sangue.

**Parâmetros:**
- `files`: Lista de arquivos PDF (multipart/form-data)

**Processo:**
1. Recebe múltiplos arquivos PDF
2. Para cada PDF:
   - Extrai a data do exame a partir do campo: DATA COLETA/RECEBIMENTO: DD/MM/AAAA HH:MM
   - Extrai os exames e seus valores numéricos (ignorando intervalos de referência)
   - Normaliza o nome dos exames (sem acento, minúsculo, sem espaços duplicados)
3. Agrega os resultados em um DataFrame (pandas)
4. Gera uma planilha Excel onde cada linha é uma data de coleta e cada coluna é um exame

**Resposta:**
- Arquivo Excel (.xlsx) para download

**Códigos de Erro:**
- `400 Bad Request`: Nenhum arquivo enviado ou nenhum dado válido extraído dos PDFs

## Modelos de Dados

### Estrutura de Dados Extraídos
```python
[
  {
    "data_coleta": "11/04/2025",
    "exames": {
      "hemoglobina": 13.5,
      "hematocrito": 38.4,
      "glicose": 93.0,
      ...
    }
  },
  ...
]
```

### Estrutura da Planilha Excel Gerada

| Data da Coleta | Hemoglobina | Hematócrito | Glicose | Creatinina | ... |
|----------------|-------------|-------------|---------|------------|-----|
| 11/04/2025     | 13,5        | 38,4        | 93,0    | 0,92       | ... |
| 14/03/2025     | 13,2        | 37,8        | 95,0    | 0,90       | ... |

## Componentes Principais

### PDFExtractor
Classe responsável pela extração de dados de exames de sangue de arquivos PDF.

**Métodos principais:**
- `extract_from_pdf(file_path)`: Extrai dados de um arquivo PDF de exame de sangue
- `_extract_collection_date(text)`: Extrai a data de coleta do texto do PDF
- `_extract_exams_and_values(text)`: Extrai os exames e seus valores do texto do PDF
- `_normalize_exam_name(name)`: Normaliza o nome do exame conforme especificação

### ExcelGenerator
Classe responsável pela geração de planilhas Excel a partir dos dados extraídos dos PDFs.

**Métodos principais:**
- `generate_excel(data_list)`: Gera uma planilha Excel a partir dos dados extraídos dos PDFs
