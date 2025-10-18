import os
import logging
from pathlib import Path
from pdf_processor import PDFProcessor
from ai_analyzer_ollama import FinancialAnalyzerOllama
from document_generator import ReportGenerator
from latex_generator import LatexGenerator
import ollama

class FinancialAnalysisSystemOllama:
    def __init__(self, input_folder="input_pdfs", output_folder="output", model_name="llama3.1:8b"):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.pdf_processor = PDFProcessor()
        self.ai_analyzer = FinancialAnalyzerOllama(model_name)
        self.report_generator = ReportGenerator()
        self.latex_generator = LatexGenerator()

        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Crear carpetas si no existen
        self.output_folder.mkdir(exist_ok=True)
    
    def process_folder(self):
        """Procesa todos los PDFs en la carpeta de entrada"""
        # Buscar PDFs en la carpeta padre/input_pdfs (nivel superior)
        pdf_files = list(Path("..").glob("input_pdfs/*.pdf"))
        
        if not pdf_files:
            self.logger.warning("No se encontraron archivos PDF en la carpeta input_pdfs")
            # Intentar en la carpeta actual por si acaso
            pdf_files = list(Path(".").glob("*.pdf"))
            if pdf_files:
                self.logger.info(f"Encontrados {len(pdf_files)} PDFs en carpeta actual")
        
        if not pdf_files:
            self.logger.error("No se encontraron archivos PDF para procesar")
            return
        
        all_extracted_data = []
        
        for pdf_file in pdf_files:
            self.logger.info(f"Procesando: {pdf_file.name}")
            
            try:
                # 1. Extraer texto del PDF
                extracted_text = self.pdf_processor.extract_text(str(pdf_file))
                
                if not extracted_text or len(extracted_text.strip()) < 50:
                    self.logger.warning(f"PDF con poco texto: {pdf_file.name}")
                    continue
                
                # 2. Analizar con Ollama
                self.logger.info(f"Enviando a Ollama para análisis: {pdf_file.name}")
                analysis_result = self.ai_analyzer.analyze_financial_content(
                    extracted_text, 
                    pdf_file.name
                )
                
                all_extracted_data.append({
                    'file_name': pdf_file.name,
                    'raw_text': extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text,
                    'analysis': analysis_result
                })
                
                self.logger.info(f"✓ Análisis completado: {pdf_file.name}")
                
            except Exception as e:
                self.logger.error(f"Error procesando {pdf_file.name}: {str(e)}")
                continue
        
        # 3. Generar documento consolidado
        if all_extracted_data:
            self.generate_final_report(all_extracted_data)
        else:
            self.logger.error("No se pudo procesar ningún PDF correctamente")
    
    def generate_final_report(self, data):
        """Genera el documento final con todos los análisis"""
        try:
            output_file = self.report_generator.generate_comprehensive_report(
                data, 
                str(self.output_folder / "analisis_financiero_ollama.docx")
            )
            self.logger.info(f"✓ Documento final generado: {output_file}")
            
            # Generar también resumen ejecutivo
            executive_summary = self.report_generator.generate_executive_summary(data)
            summary_file = self.output_folder / "resumen_ejecutivo_ollama.txt"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(executive_summary)
            
            self.logger.info(f"✓ Resumen ejecutivo generado: {summary_file}")
            
            # Generar JSON con todos los datos para análisis posterior
            json_file = self.output_folder / "datos_completos.json"
            import json
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            latex_file = self.latex_generator.generate_corporate_report(
                data, 
                str(self.output_folder / "informe_corporativo.tex")
            )
            self.logger.info(f"✓ Documento LaTeX generado: {latex_file}")
            
        except Exception as e:
            self.logger.error(f"Error generando reporte final: {str(e)}")

def main():
    """Función principal con selección de modelo"""
    print("=== Sistema de Análisis Financiero con Ollama ===")
    
    # Listar modelos disponibles
    try:
        models = ollama.list()
        print("✓ Ollama conectado correctamente")
        
        # CORRECCIÓN: Acceder correctamente a los modelos usando .models
        available_models = [model.model for model in models.models]
        
        print(f"\nModelos disponibles en Ollama: {len(available_models)}")
        for i, model in enumerate(available_models, 1):
            print(f"{i}. {model}")
        
        if available_models:
            selection = input(f"\nSelecciona modelo (1-{len(available_models)}, Enter para 1): ").strip()
            if selection.isdigit() and 1 <= int(selection) <= len(available_models):
                model_name = available_models[int(selection) - 1]
            else:
                model_name = available_models[0]  # Usar el primero por defecto
        else:
            print("No hay modelos disponibles. Instala uno con: ollama pull llama3.1:8b")
            return
            
    except Exception as e:
        print(f"Error conectando con Ollama: {e}")
        print("Asegúrate de que Ollama esté instalado y corriendo")
        print("Puedes verificar con: ollama list")
        return
    
    print(f"\nUsando modelo: {model_name}")
    print("Iniciando procesamiento...\n")
    
    # Iniciar sistema
    system = FinancialAnalysisSystemOllama(model_name=model_name)
    system.process_folder()

if __name__ == "__main__":
    main()