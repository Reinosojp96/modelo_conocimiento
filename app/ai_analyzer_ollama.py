import ollama
import json
import logging
from typing import Dict, Any, List

class FinancialAnalyzerOllama:
    def __init__(self, model_name="llama3.1:8b"):
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)
        
        # Verificar que Ollama esté corriendo
        self._check_ollama_connection()
    
    def _check_ollama_connection(self):
        """Verifica que Ollama esté funcionando"""
        try:
            models = ollama.list()
            self.logger.info("✓ Ollama conectado correctamente")
            
            # CORRECCIÓN: Acceder correctamente a los modelos usando .models
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
    
    def analyze_financial_content(self, text: str, filename: str) -> Dict[str, Any]:
        """Analiza el contenido financiero usando Ollama"""
        
        try:
            # Limitar el texto para evitar tokens excesivos
            limited_text = text[:4000]  # Más conservador
            
            prompt = self._create_analysis_prompt(limited_text, filename)
            
            self.logger.info(f"Enviando prompt a Ollama (modelo: {self.model_name})...")
            
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.1,
                    'top_p': 0.9,
                    'num_predict': 1500  # Reducido para mayor estabilidad
                }
            )
            
            analysis_text = response['response']
            self.logger.info("✓ Respuesta recibida de Ollama")
            
            return self._parse_analysis_response(analysis_text)
            
        except Exception as e:
            self.logger.error(f"Error en análisis con Ollama: {e}")
            return self._fallback_analysis(text, filename)
    
    def _create_analysis_prompt(self, text: str, filename: str) -> str:
        """Crea el prompt optimizado para análisis completo con elementos gráficos"""
        return f"""Eres un analista financiero experto. Analiza este documento y devuelve SOLO un JSON válido.

DOCUMENTO: {filename}
CONTENIDO: {text}

ANÁLISIS REQUERIDO (formato JSON):
{{
  "resumen_ejecutivo": "resumen ejecutivo de 3-4 líneas",
  "puntos_fuertes": ["punto 1", "punto 2", "punto 3", "punto 4"],
  "areas_mejora": ["área 1", "área 2", "área 3", "área 4"],
  "recomendaciones": ["recomendación 1", "recomendación 2", "recomendación 3"],
  "riesgo_asociado": "bajo/medio/alto",
  "metricas_principales": {{
    "ingresos": "información detectada",
    "gastos": "información detectada", 
    "utilidades": "información detectada",
    "flujo_caja": "información detectada"
  }},
  "procesos_identificados": ["proceso 1", "proceso 2", "proceso 3"],
  "relaciones_departamentales": ["relación 1", "relación 2"],
  "terminos_financieros_clave": ["término 1", "término 2", "término 3", "término 4"]
}}

Responde EXCLUSIVAMENTE con el JSON, sin texto adicional.
"""
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parsea la respuesta de Ollama"""
        try:
            # Limpiar la respuesta
            cleaned_text = response_text.strip()
            
            # Buscar JSON entre llaves
            start = cleaned_text.find('{')
            end = cleaned_text.rfind('}') + 1
            
            if start != -1 and end != 0:
                json_str = cleaned_text[start:end]
                return json.loads(json_str)
            else:
                # Si no encuentra JSON, crear uno básico
                self.logger.warning("No se pudo extraer JSON de la respuesta")
                return self._create_basic_analysis(response_text)
                
        except Exception as e:
            self.logger.warning(f"Error parseando JSON: {e}")
            return self._create_basic_analysis(response_text)
    
    def _create_basic_analysis(self, text: str) -> Dict[str, Any]:
        """Crea un análisis básico a partir del texto"""
        return {
            "resumen_ejecutivo": text[:200] + "..." if len(text) > 200 else text,
            "puntos_fuertes": ["Análisis completado con IA local"],
            "areas_mejora": ["Validar resultados manualmente"],
            "recomendaciones": ["Revisar documento original"],
            "riesgo_asociado": "medio",
            "metricas_principales": {
                "ingresos": "No detectado",
                "gastos": "No detectado", 
                "utilidades": "No detectado",
                "flujo_caja": "No detectado"
            },
            "procesos_identificados": ["Proceso genérico"],
            "relaciones_departamentales": ["Relación básica"],
            "terminos_financieros_clave": ["Término general"]
        }
    
    def _fallback_analysis(self, text: str, filename: str) -> Dict[str, Any]:
        """Análisis de fallback cuando Ollama falla"""
        return {
            "resumen_ejecutivo": f"Documento {filename} procesado. Falló el análisis con IA.",
            "puntos_fuertes": ["Procesamiento básico completado"],
            "areas_mejora": ["Error en análisis IA"],
            "recomendaciones": ["Reintentar o validar manualmente"],
            "riesgo_asociado": "medio",
            "metricas_principales": {
                "ingresos": "No disponible",
                "gastos": "No disponible", 
                "utilidades": "No disponible",
                "flujo_caja": "No disponible"
            },
            "procesos_identificados": ["No identificados"],
            "relaciones_departamentales": ["No identificadas"],
            "terminos_financieros_clave": ["No identificados"]
        }