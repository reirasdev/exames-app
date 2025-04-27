import os
import sys
import unittest
from pdf_extractor import PDFExtractor

class TestPDFExtractor(unittest.TestCase):
    """
    Testes unitários para a classe PDFExtractor.
    """
    
    def setUp(self):
        self.extractor = PDFExtractor()
        self.test_pdf_path = "/home/ubuntu/upload/sangue-11_04_2025.pdf"
    
    def test_extract_from_pdf(self):
        """Testa a extração completa de dados do PDF."""
        if not os.path.exists(self.test_pdf_path):
            self.skipTest("Arquivo de teste não encontrado")
            
        result = self.extractor.extract_from_pdf(self.test_pdf_path)
        
        # Verificar se o resultado não é None
        self.assertIsNotNone(result)
        
        # Verificar se a data de coleta foi extraída corretamente
        self.assertEqual(result["data_coleta"], "11/04/2025")
        
        # Verificar se alguns exames esperados foram extraídos
        exams = result["exames"]
        self.assertGreater(len(exams), 0)
        
        # Imprimir os exames extraídos para debug
        print("Exames extraídos:")
        for name, value in exams.items():
            print(f"{name}: {value}")
    
    def test_normalize_exam_name(self):
        """Testa a normalização dos nomes dos exames."""
        test_cases = [
            ("Hemoglobina", "hemoglobina"),
            ("Ácido Úrico", "acido urico"),
            ("Transaminase  pirúvica", "transaminase piruvica"),
            ("CREATININA", "creatinina")
        ]
        
        for original, expected in test_cases:
            result = self.extractor._normalize_exam_name(original)
            self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
