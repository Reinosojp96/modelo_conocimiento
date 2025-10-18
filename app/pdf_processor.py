import pdfplumber
import PyPDF2
import re
from typing import List, Dict, Any

class PDFProcessor:
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text(self, pdf_path: str) -> str:
        """Extrae texto de un archivo PDF usando múltiples métodos"""
        text = ""
        
        try:
            # Método 1: pdfplumber (mejor para PDFs con tablas)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            # Si pdfplumber no extrajo suficiente texto, usar PyPDF2 como respaldo
            if len(text.strip()) < 100:
                text = self._extract_with_pypdf2(pdf_path)
                
        except Exception as e:
            print(f"Error con pdfplumber: {e}, usando PyPDF2 como respaldo")
            text = self._extract_with_pypdf2(pdf_path)
        
        return self.clean_text(text)
    
    def _extract_with_pypdf2(self, pdf_path: str) -> str:
        """Extrae texto usando PyPDF2 como método alternativo"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error con PyPDF2: {e}")
        
        return text
    
    def clean_text(self, text: str) -> str:
        """Limpia y normaliza el texto extraído"""
        # Remover múltiples espacios y saltos de línea
        text = re.sub(r'\s+', ' ', text)
        # Remover caracteres especiales problemáticos
        text = re.sub(r'[^\x00-\x7FáéíóúÁÉÍÓÚñÑ¿¡°$%&/\-.,;:()]', ' ', text)
        return text.strip()
    
    def extract_tables(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extrae tablas de PDFs (útil para datos financieros estructurados)"""
        tables = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()
                    for table_num, table in enumerate(page_tables):
                        if table and any(any(cell for cell in row) for row in table):
                            tables.append({
                                'page': page_num + 1,
                                'table_number': table_num + 1,
                                'data': table
                            })
        except Exception as e:
            print(f"Error extrayendo tablas: {e}")
        
        return tables