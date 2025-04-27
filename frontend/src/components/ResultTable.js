import React from 'react';
import './ResultTable.css';

function ResultTable({ data }) {
  if (!data || !data.headers || !data.rows) {
    return <p>Nenhum dado disponível para exibição.</p>;
  }

  return (
    <div className="result-table-container">
      <table className="result-table">
        <thead>
          <tr>
            {data.headers.map((header, index) => (
              <th key={index}>{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.rows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, cellIndex) => (
                <td key={cellIndex}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ResultTable;
