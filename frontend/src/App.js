import React, { useState, useEffect } from 'react';
import FileUploader from './components/FileUploader';
import ResultTable from './components/ResultTable';
import './App.css';

function App() {
  const [files, setFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [tableData, setTableData] = useState(null);
  const [error, setError] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState(null);

  const handleFileChange = (selectedFiles) => {
    setFiles(selectedFiles);
    setError(null);
    setDownloadUrl(null);
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      setError('Por favor, selecione pelo menos um arquivo PDF.');
      return;
    }

    setIsUploading(true);
    setError(null);
    setDownloadUrl(null);

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erro ao processar os arquivos.');
      }

      // Criar URL para download do arquivo
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      setDownloadUrl(url);

      // Simular dados da tabela para visualização
      // Em uma implementação real, você poderia extrair esses dados do Excel
      setTableData({
        headers: ['Data da Coleta', 'Hemoglobina', 'Hematócrito', 'Glicose', 'Creatinina'],
        rows: [
          ['11/04/2025', '13.5', '38.4', '93', '0.92'],
          ['14/03/2025', '13.2', '37.8', '95', '0.90'],
          ['29/01/2025', '13.0', '37.5', '92', '0.88'],
        ]
      });
    } catch (err) {
      setError(err.message);
      console.error('Erro:', err);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Sistema de Processamento de Exames de Sangue</h1>
        <p>Faça upload de PDFs de exames para gerar uma planilha Excel com série temporal</p>
      </header>

      <main className="app-main">
        <FileUploader 
          files={files} 
          onFileChange={handleFileChange} 
          onUpload={handleUpload}
          isUploading={isUploading}
        />

        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}

        {downloadUrl && (
          <div className="download-section">
            <h2>Download Disponível</h2>
            <p>Sua planilha Excel foi gerada com sucesso!</p>
            <a 
              href={downloadUrl} 
              download="exames.xlsx" 
              className="download-button"
            >
              Baixar Planilha Excel
            </a>
          </div>
        )}

        {tableData && (
          <div className="result-section">
            <h2>Visualização dos Dados</h2>
            <ResultTable data={tableData} />
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Sistema de Processamento de Exames de Sangue © 2025</p>
      </footer>
    </div>
  );
}

export default App;
