# pdf_processor_advanced.py
import pdfplumber
import PyPDF2
import re
from typing import List, Dict, Any

class PDFProcessorAdvanced:
    def __init__(self, max_chars_per_chunk=6000, overlap_chars=500):
        self.max_chars_per_chunk = max_chars_per_chunk
        self.overlap_chars = overlap_chars
    
    def extract_text_intelligent(self, pdf_path: str) -> str:
        """Extrae texto inteligente de PDFs grandes"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            # Si es muy grande, usar estrategia de chunks
            if len(text) > 10000:
                text = self._extract_structured_content(pdf_path)
                
        except Exception as e:
            print(f"Error con pdfplumber: {e}, usando PyPDF2")
            text = self._extract_with_pypdf2(pdf_path)
        
        return self.clean_text(text)
    
    def extract_text_by_chunks(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extrae texto en chunks inteligentes para análisis por partes"""
        full_text = self.extract_text_intelligent(pdf_path)
        
        if len(full_text) <= self.max_chars_per_chunk:
            return [{"chunk": 1, "content": full_text, "pages": "all"}]
        
        # Dividir en chunks con overlap
        chunks = []
        start = 0
        chunk_num = 1
        
        while start < len(full_text):
            end = start + self.max_chars_per_chunk
            chunk_content = full_text[start:end]
            
            # Intentar dividir en párrafos naturales
            if end < len(full_text):
                last_period = chunk_content.rfind('.')
                if last_period > self.max_chars_per_chunk * 0.7:
                    chunk_content = chunk_content[:last_period + 1]
                    end = start + len(chunk_content)
            
            chunks.append({
                "chunk": chunk_num,
                "content": chunk_content,
                "pages": f"approx_{(chunk_num-1)*10+1}-{chunk_num*10}"
            })
            
            start = end - self.overlap_chars  # Overlap para contexto
            chunk_num += 1
        
        return chunks
    
    def _extract_structured_content(self, pdf_path: str) -> str:
        """Extrae contenido estructurado de PDFs grandes"""
        structured_text = ""
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Extraer tablas
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            structured_text += f"\n[TABLE_PAGE_{page_num+1}]\n"
                            for row in table:
                                structured_text += " | ".join([str(cell) for cell in row if cell]) + "\n"
                    
                    # Extraer texto con estructura
                    text = page.extract_text()
                    if text:
                        lines = text.split('\n')
                        for line in lines:
                            if len(line.strip()) > 0:
                                if (line.isupper() and len(line) < 100) or \
                                   (len(line.strip()) < 50 and any(c.isupper() for c in line)):
                                    structured_text += f"\nSECTION: {line.strip()}\n"
                                else:
                                    structured_text += line + " "
        
        except Exception as e:
            print(f"Error en extracción estructurada: {e}")
            structured_text = self._extract_with_pypdf2(pdf_path)
        
        return structured_text
    
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
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\x00-\x7FáéíóúÁÉÍÓÚñÑ¿¡°$%&/\-.,;:()]', ' ', text)
        return text.strip()