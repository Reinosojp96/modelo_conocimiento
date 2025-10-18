# main_enterprise.py (corregido)
import os
import logging
from pathlib import Path
from pdf_processor_advanced import PDFProcessorAdvanced
from ai_analyzer_enterprise import FinancialAnalyzerEnterprise
from latex_generator import LatexGenerator
import ollama

class EnterpriseFinancialAnalysisSystem:
    def __init__(self, input_folder="../input_pdfs", output_folder="output", model_name="llama3.1:8b"):
        # CAMBIO: "../input_pdfs" en lugar de "input_pdfs"
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.pdf_processor = PDFProcessorAdvanced()
        self.ai_analyzer = FinancialAnalyzerEnterprise(model_name)
        self.latex_generator = LatexGenerator()
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.output_folder.mkdir(exist_ok=True)
    
    def process_enterprise_folder(self):
        """Procesa carpeta con documentos empresariales grandes"""
        pdf_files = list(self.input_folder.glob("*.pdf"))
        
        if not pdf_files:
            self.logger.error(f"No se encontraron PDFs en: {self.input_folder.absolute()}")
            # Mostrar qué hay en la carpeta
            if self.input_folder.exists():
                self.logger.info(f"Contenido de {self.input_folder}:")
                for item in self.input_folder.iterdir():
                    self.logger.info(f"  - {item.name}")
            return
        
        all_analyses = []
        
        for pdf_file in pdf_files:
            file_size_mb = pdf_file.stat().st_size / (1024 * 1024)
            self.logger.info(f"Procesando: {pdf_file.name} ({file_size_mb:.1f} MB)")
            
            try:
                # Extraer en chunks para documentos grandes
                chunks = self.pdf_processor.extract_text_by_chunks(str(pdf_file))
                self.logger.info(f"Documento dividido en {len(chunks)} chunks")
                
                # Analizar documento completo
                analysis = self.ai_analyzer.analyze_large_document(chunks, pdf_file.name)
                
                all_analyses.append({
                    'file_name': pdf_file.name,
                    'file_size_mb': file_size_mb,
                    'chunks_processed': len(chunks),
                    'analysis': analysis
                })
                
                self.logger.info(f"✓ Análisis completado: {pdf_file.name}")
                
            except Exception as e:
                self.logger.error(f"Error procesando {pdf_file.name}: {e}")
                continue
        
        if all_analyses:
            self.generate_enterprise_report(all_analyses)
    
    def generate_enterprise_report(self, data):
        """Genera reporte empresarial completo"""
        try:
            # Generar LaTeX empresarial
            latex_file = self.latex_generator.generate_corporate_report(
                data, 
                str(self.output_folder / "informe_empresarial_consolidado.tex")
            )
            self.logger.info(f"✓ Reporte LaTeX generado: {latex_file}")
            
            # Generar JSON con metadatos
            import json
            json_file = self.output_folder / "analisis_empresarial_completo.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"✓ Datos completos exportados: {json_file}")
            
            # Estadísticas del procesamiento
            total_size = sum(item['file_size_mb'] for item in data)
            total_chunks = sum(item['chunks_processed'] for item in data)
            self.logger.info(f"📊 Resumen: {len(data)} documentos, {total_size:.1f} MB, {total_chunks} chunks procesados")
            
        except Exception as e:
            self.logger.error(f"Error generando reporte: {e}")

# Ejecución
if __name__ == "__main__":
    system = EnterpriseFinancialAnalysisSystem()
    system.process_enterprise_folder()