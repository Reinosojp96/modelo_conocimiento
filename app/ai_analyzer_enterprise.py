import ollama
import json
import logging
from typing import Dict, Any, List

class FinancialAnalyzerEnterprise:
    def __init__(self, model_name="llama3.1:8b"):
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)
        self._check_ollama_connection()  # ✅ Método añadido
    
    def _check_ollama_connection(self):
        """Verifica que Ollama esté funcionando"""
        try:
            models = ollama.list()
            self.logger.info("✓ Ollama conectado correctamente")
            
            available_models = [model.model for model in models.models]
            
            if available_models:
                self.logger.info(f"Modelos disponibles: {len(available_models)}")
                if self.model_name not in available_models:
                    self.logger.warning(f"Modelo {self.model_name} no encontrado. Usando {available_models[0]}")
                    self.model_name = available_models[0]
            else:
                self.logger.warning("No se pudieron listar modelos")
                    
        except Exception as e:
            self.logger.error(f"Error conectando con Ollama: {e}")
            raise
    
    def analyze_large_document(self, chunks: List[Dict], filename: str) -> Dict[str, Any]:
        """Analiza documentos grandes por chunks y consolida"""
        chunk_analyses = []
        
        for chunk in chunks:
            self.logger.info(f"Analizando chunk {chunk['chunk']} de {filename}")
            chunk_analysis = self.analyze_chunk(chunk['content'], filename, chunk['chunk'])
            chunk_analyses.append(chunk_analysis)
        
        # Consolidar análisis de todos los chunks
        return self._consolidate_chunk_analyses(chunk_analyses, filename)
    
    def analyze_chunk(self, text: str, filename: str, chunk_num: int) -> Dict[str, Any]:
        """Analiza un chunk individual del documento"""
        try:
            prompt = self._create_chunk_prompt(text, filename, chunk_num)
            
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.1,
                    'top_p': 0.9,
                    'num_predict': 2000
                }
            )
            
            analysis_text = response['response']
            return self._parse_analysis_response(analysis_text)
            
        except Exception as e:
            self.logger.error(f"Error analizando chunk {chunk_num}: {e}")
            return self._fallback_chunk_analysis()
    
    def _create_chunk_prompt(self, text: str, filename: str, chunk_num: int) -> str:
        """Crea prompt para análisis de chunk"""
        return f"""Eres un analista financiero experto. Analiza ESTA PARTE de un documento grande.

DOCUMENTO: {filename} (Parte {chunk_num})
CONTENIDO: {text[:5000]}

Proporciona un análisis JSON de ESTA SECCIÓN específica:

{{
  "resumen_seccion": "resumen de 2-3 líneas de esta parte",
  "metricas_detectadas": ["métrica1", "métrica2"],
  "procesos_mencionados": ["proceso1", "proceso2"],
  "riesgos_identificados": ["riesgo1", "riesgo2"],
  "recomendaciones_seccion": ["recomendación1", "recomendación2"],
  "terminos_clave": ["término1", "término2", "término3"]
}}

Responde SOLO con JSON válido.
"""
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parsea la respuesta de Ollama"""
        try:
            cleaned_text = response_text.strip()
            start = cleaned_text.find('{')
            end = cleaned_text.rfind('}') + 1
            
            if start != -1 and end != 0:
                json_str = cleaned_text[start:end]
                return json.loads(json_str)
            else:
                self.logger.warning("No se pudo extraer JSON de la respuesta")
                return self._fallback_chunk_analysis()
                
        except Exception as e:
            self.logger.warning(f"Error parseando JSON: {e}")
            return self._fallback_chunk_analysis()
    
    def _consolidate_chunk_analyses(self, chunk_analyses: List[Dict], filename: str) -> Dict[str, Any]:
        """Consolida análisis de múltiples chunks"""
        try:
            consolidation_data = {
                "documento": filename,
                "total_chunks": len(chunk_analyses),
                "analisis_chunks": chunk_analyses
            }
            
            prompt = f"""Eres un director financiero senior. Consolida estos análisis parciales en un informe ejecutivo completo.

DOCUMENTO: {filename}
TOTAL DE PARTES ANALIZADAS: {len(chunk_analyses)}
ANÁLISIS POR PARTES: {json.dumps(chunk_analyses, ensure_ascii=False)}

Genera un informe ejecutivo consolidado en formato JSON:

{{
  "resumen_ejecutivo_consolidado": "resumen ejecutivo completo de 5-10 líneas",
  "hallazgos_principales": ["hallazgo1", "hallazgo2", "hallazgo3", "hallazgo4", "hallazgo5"],
  "metricas_financieras_consolidadas": {{
    "ingresos_totales": "análisis consolidado",
    "gastos_operativos": "análisis consolidado",
    "margen_utilidad": "análisis consolidado",
    "flujo_efectivo": "análisis consolidado",
    "patrimonio": "análisis consolidado"
  }},
  "riesgos_prioritarios": ["riesgo1", "riesgo2", "riesgo3", "riesgo4"],
  "recomendaciones_estrategicas": ["recomendación1", "recomendación2", "recomendación3", "recomendación4"],
  "procesos_criticos": ["proceso1", "proceso2", "proceso3"],
  "oportunidades_identificadas": ["oportunidad1", "oportunidad2", "oportunidad3"]
}}

Nivel de riesgo general (bajo/medio/alto):"""
            
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.1,
                    'top_p': 0.9,
                    'num_predict': 3000
                }
            )
            
            consolidated_analysis = json.loads(response['response'])
            return consolidated_analysis
            
        except Exception as e:
            self.logger.error(f"Error consolidando análisis: {e}")
            return self._fallback_consolidation(chunk_analyses, filename)
    
    def _fallback_chunk_analysis(self) -> Dict[str, Any]:
        """Análisis de fallback para chunks"""
        return {
            "resumen_seccion": "Análisis básico completado",
            "metricas_detectadas": ["No detectadas en esta sección"],
            "procesos_mencionados": ["No identificados"],
            "riesgos_identificados": ["No especificados"],
            "recomendaciones_seccion": ["Validar manualmente"],
            "terminos_clave": ["Generales"]
        }
    
    def _fallback_consolidation(self, chunk_analyses: List[Dict], filename: str) -> Dict[str, Any]:
        """Consolidación de fallback"""
        return {
            "resumen_ejecutivo_consolidado": f"Documento {filename} procesado con análisis básico de {len(chunk_analyses)} partes.",
            "hallazgos_principales": ["Procesamiento completado", "Validación manual recomendada"],
            "metricas_financieras_consolidadas": {
                "ingresos_totales": "No consolidado",
                "gastos_operativos": "No consolidado",
                "margen_utilidad": "No consolidado",
                "flujo_efectivo": "No consolidado",
                "patrimonio": "No consolidado"
            },
            "riesgos_prioritarios": ["Riesgo de procesamiento"],
            "recomendaciones_estrategicas": ["Revisar análisis manualmente"],
            "procesos_criticos": ["Procesamiento documental"],
            "oportunidades_identificadas": ["Automatización mejorada"]
        }