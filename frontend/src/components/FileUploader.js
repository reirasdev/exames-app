import React, { useRef } from 'react';
import './FileUploader.css';

function FileUploader({ files, onFileChange, onUpload, isUploading }) {
  const fileInputRef = useRef(null);

  const handleFileInputChange = (e) => {
    onFileChange(Array.from(e.target.files));
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFileChange(Array.from(e.dataTransfer.files));
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="file-uploader">
      <div 
        className="drop-area"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={handleBrowseClick}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileInputChange}
          accept=".pdf"
          multiple
          style={{ display: 'none' }}
        />
        <div className="drop-message">
          <i className="file-icon">📄</i>
          <p>Arraste e solte arquivos PDF aqui ou clique para selecionar</p>
        </div>
      </div>

      {files.length > 0 && (
        <div className="file-list">
          <h3>Arquivos Selecionados ({files.length})</h3>
          <ul>
            {files.map((file, index) => (
              <li key={index}>
                <span className="file-name">{file.name}</span>
                <span className="file-size">({(file.size / 1024).toFixed(2)} KB)</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <button 
        className="upload-button"
        onClick={onUpload}
        disabled={isUploading || files.length === 0}
      >
        {isUploading ? 'Processando...' : 'Processar PDFs'}
      </button>
    </div>
  );
}

export default FileUploader;
