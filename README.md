# Sistema de Processamento de Exames de Sangue

Um sistema web completo para processamento de exames de sangue em PDF, que extrai dados de exames e gera planilhas Excel em formato de série temporal.

## Funcionalidades

- Upload de múltiplos arquivos PDF de exames de sangue
- Extração automática da data de coleta, nomes dos exames e valores numéricos
- Geração de planilha Excel no formato de série temporal (linhas = datas, colunas = tipos de exame)
- Visualização dos dados extraídos em tabela
- Download da planilha Excel gerada

## Estrutura do Projeto

```
/exames-app
  /frontend         # Frontend em React
  /backend          # Backend em Python/FastAPI
  /data             # Diretório para armazenamento temporário de dados
  Dockerfile        # Configuração para containerização
  Procfile          # Configuração para deploy no Heroku
  README.md         # Este arquivo
```

## Requisitos

- Docker
- Node.js 14+ (para desenvolvimento)
- Python 3.8+ (para desenvolvimento)

## Instruções de Uso

### Execução com Docker Compose
1. docker compose down

2. docker compose build --no-cache

3. docker compose up -d

   ### Para acompanhar os logs
   1.  docker compose logs -f


### Execução com Docker

1. Clone o repositório
2. Construa a imagem Docker:
   ```
   docker build -t exames-app .
   ```
3. Execute o container:
   ```
   docker run -p 8000:8000 exames-app
   ```
4. Acesse a aplicação em `http://localhost:8000`

### Desenvolvimento Local

#### Backend (Python/FastAPI)

1. Navegue até o diretório do backend:
   ```
   cd backend
   ```
2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Execute o servidor de desenvolvimento:
   ```
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend (React)

1. Navegue até o diretório do frontend:
   ```
   cd frontend
   ```
2. Instale as dependências:
   ```
   npm install
   ```
3. Execute o servidor de desenvolvimento:
   ```
   npm start
   ```
4. Acesse o frontend em `http://localhost:3000`

## Deploy no Heroku

1. Instale o Heroku CLI
2. Faça login no Heroku:
   ```
   heroku login
   ```
3. Crie um novo aplicativo Heroku:
   ```
   heroku create seu-app-name
   ```
4. Configure o buildpack:
   ```
   heroku buildpacks:set heroku/python
   ```
5. Faça o deploy:
   ```
   git push heroku main
   ```

## Tecnologias Utilizadas

- **Backend**: Python, FastAPI, pdfplumber, pandas, openpyxl
- **Frontend**: React, Webpack, Babel, CSS
- **Containerização**: Docker
- **Deploy**: Heroku

## Licença

Este projeto está licenciado sob a licença MIT.
