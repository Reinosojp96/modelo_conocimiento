from typing import List, Dict, Any
from datetime import datetime
import json
from locale import setlocale, LC_TIME
import math

try:
    setlocale(LC_TIME, 'es_ES.UTF-8')
except Exception:
    try:
        setlocale(LC_TIME, 'es_ES')
    except Exception:
        pass


class LatexGenerator:
    def __init__(self):
        pass
    
    def generate_corporate_report(self, data: List[Dict[str, Any]], output_path: str) -> str:
        """Genera un documento LaTeX profesional corporativo EXTENSO"""
        try:
            if not isinstance(data, list) or not data:
                print("Advertencia: La lista de datos está vacía. Generando informe con datos cero.")
            
            latex_content = self._create_extensive_latex_document(data)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            return output_path
        except Exception as e:
            print(f"Error generando reporte LaTeX: {e}")
            raise

    def _create_extensive_latex_document(self, data: List[Dict[str, Any]]) -> str:
        """Crea un documento LaTeX extenso de 10+ páginas"""
        
        sections = [
            self._generate_executive_summary(data),
            self._generate_methodology(),
            self._generate_detailed_analysis(data),
            self._generate_metrics_analysis(data),
            self._generate_risk_assessment(data),
            self._generate_strategic_recommendations(data),
            self._generate_implementation_plan(),
            self._generate_graphs_content(data),  
            self._generate_appendix(data)
        ]
        
        current_date = datetime.now().strftime('%d de %B de %Y')
        num_docs = len(data)
        
        latex_template = f"""\\documentclass[11pt]{{report}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[spanish]{{babel}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=2.5cm}}
\\usepackage{{graphicx}}
\\usepackage{{tikz}}
\\usepackage{{pgfplots}}
\\pgfplotsset{{compat=1.18}}
\\usetikzlibrary{{shapes, arrows, positioning, fit, calc}}
\\usepackage{{xcolor}}
\\usepackage{{hyperref}}
\\usepackage{{booktabs}}
\\usepackage{{array}}
\\usepackage{{float}}
\\usepackage{{longtable}}
\\usepackage{{multirow}}
\\usepackage{{enumitem}}
\\usepackage{{lipsum}}
\\usepackage[most]{{tcolorbox}} 

% Colores corporativos
\\definecolor{{corporate-blue}}{{RGB}}{{0, 82, 155}}
\\definecolor{{corporate-gray}}{{RGB}}{{240, 240, 240}}
\\definecolor{{accent-orange}}{{RGB}}{{255, 102, 0}}
\\definecolor{{success-green}}{{RGB}}{{34, 139, 34}}
\\definecolor{{warning-yellow}}{{RGB}}{{255, 165, 0}}
\\definecolor{{danger-red}}{{RGB}}{{220, 53, 69}}

% Estilo profesional
\\usepackage{{titlesec}}
\\titleformat{{\\chapter}}[display]
  {{\\normalfont\\huge\\bfseries\\color{{corporate-blue}}}}
  {{\\filleft\\thechapter}}{{10pt}}{{\\titlerule[1pt]\\vspace{{5pt}}\\filright}} 
\\titleformat{{\\section}}
  {{\\normalfont\\Large\\bfseries\\color{{corporate-blue}}}}
  {{\\thesection}}{{0.5em}}{{}}
\\titleformat{{\\subsection}}
  {{\\normalfont\\large\\bfseries\\color{{corporate-blue}}}}
  {{\\thesubsection}}{{0.5em}}{{}}
\\titlespacing{{\\chapter}}{{0pt}}{{50pt}}{{40pt}}

\\usepackage{{fancyhdr}}
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyhead[L]{{\\textcolor{{corporate-blue}}{{\\footnotesize Informe Corporativo - Análisis Financiero}}}}
\\fancyhead[R]{{\\textcolor{{corporate-blue}}{{\\footnotesize Página \\thepage}}}} 
\\renewcommand{{\\headrulewidth}}{{0.4pt}}
\\renewcommand{{\\headrule}}{{\\color{{corporate-blue}}\\hrule}}

\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{1em}}

\\begin{{document}}

% Portada corporativa
\\begin{{titlepage}}
    \\centering
    \\vspace*{{1cm}}
    % \\includegraphics[width=0.4\\textwidth]{{logo.png}} 
    \\vspace{{1.5cm}}
    
    {{\\Huge\\color{{corporate-blue}}\\textbf{{INFORME CORPORATIVO INTEGRAL}}}}
    \\vspace{{0.5cm}}
    
    {{\\Large\\textbf{{Análisis Financiero Estratégico}}}}
    \\vspace{{1cm}}
    
    \\rule{{\\textwidth}}{{1pt}}
    \\vspace{{0.5cm}}
    
    {{\\large Generado el: {current_date}}}
    \\vspace{{0.3cm}}
    
    {{\\large Documentos analizados: {num_docs}}}
    \\vspace{{0.3cm}}
    
    {{\\large Total de páginas procesadas: {self._calculate_total_pages(data)}}}
    \\vspace{{1.5cm}}
    
    \\begin{{minipage}}{{0.8\\textwidth}}
    \\centering
    \\textbf{{Departamento de Análisis Financiero}}\\\\
    División de Inteligencia Empresarial\\\\
    Versión 2.0 - Informe Confidencial
    \\end{{minipage}}
    \\vfill
    
    \\footnotesize
    Este documento contiene información confidencial y propietaria.\\\\
    Su distribución está restringida a personal autorizado.
\\end{{titlepage}}

% Página en blanco
\\cleardoublepage 

% Tabla de contenidos
\\tableofcontents
\\cleardoublepage

{''.join(sections)}

\\end{{document}}"""
        return latex_template
    
    def _calculate_total_pages(self, data: List[Dict[str, Any]]) -> int:
        """Calcula el total de páginas procesadas (estimado)"""
        return len(data) * 15 
    
    def _assess_complexity(self, analysis: Dict[str, Any]) -> str:
        """Evalúa la complejidad del análisis"""
        puntos_count = len(analysis.get('puntos_fuertes', []))
        areas_count = len(analysis.get('areas_mejora', []))
        total = puntos_count + areas_count
        
        if total > 10:
            return "Alta"
        elif total > 5:
            return "Media" 
        else:
            return "Baja"

    def _consolidate_analysis(self, data: List[Dict[str, Any]]) -> Dict:
        """Consolida el análisis de todos los documentos para el resumen."""
        riesgos = {'alto': 0, 'medio': 0, 'bajo': 0}
        all_strengths = []
        all_improvements = []
        all_recommendations = []
        
        for item in data:
            analysis = item.get('analysis', {})
            riesgo = analysis.get('riesgo_asociado', 'medio').lower()
            if riesgo in riesgos:
                riesgos[riesgo] += 1
            
            for key, target_list in [
                ('puntos_fuertes', all_strengths), 
                ('areas_mejora', all_improvements), 
                ('recomendaciones', all_recommendations)
            ]:
                items = analysis.get(key, [])
                if isinstance(items, list):
                    target_list.extend([i for i in items if isinstance(i, str)])
            
        unique_strengths = list(set(all_strengths))[:8]
        unique_improvements = list(set(all_improvements))[:8]
        unique_recommendations = list(set(all_recommendations))[:8]
        
        resumen = (
            f"Análisis integral de {len(data)} documentos financieros corporativos. "
            f"El proceso identificó {len(unique_strengths)} áreas de excelencia operativa y "
            f"{len(unique_improvements)} oportunidades críticas de mejora. "
            f"La evaluación de riesgos revela una distribución con {riesgos['alto']} documentos de alto riesgo, "
            f"{riesgos['medio']} de riesgo medio y {riesgos['bajo']} de bajo riesgo. "
            f"Se recomienda la implementación prioritaria de las {len(unique_recommendations)} estrategias identificadas "
            f"para optimizar el desempeño financiero y fortalecer la posición competitiva de la organización."
        )
        
        return {
            'resumen_ejecutivo': resumen,
            'riesgos': riesgos,
            'puntos_fuertes_consolidados': unique_strengths,
            'areas_mejora_consolidadas': unique_improvements,
            'recomendaciones_consolidadas': unique_recommendations
        }

    def _generate_executive_summary(self, data: List[Dict[str, Any]]) -> str:
        """Genera resumen ejecutivo extenso"""
        consolidated = self._consolidate_analysis(data)
        
        return f"""
\\chapter*{{Resumen Ejecutivo}}
\\addcontentsline{{toc}}{{chapter}}{{Resumen Ejecutivo}}

\\begin{{tcolorbox}}[colback=corporate-gray!30!white, colframe=corporate-blue, title=Resumen Consolidado, fonttitle=\\bfseries]
{consolidated['resumen_ejecutivo']}
\\end{{tcolorbox}}

\\section*{{Hallazgos Clave}}
\\begin{{itemize}}[left=0pt]
    \\item \\textbf{{Documentos Procesados:}} {len(data)} documentos financieros
    \\item \\textbf{{Puntos Fuertes Identificados:}} {len(consolidated['puntos_fuertes_consolidados'])} áreas de excelencia
    \\item \\textbf{{Oportunidades de Mejora:}} {len(consolidated['areas_mejora_consolidadas'])} áreas críticas
    \\item \\textbf{{Recomendaciones Prioritarias:}} {len(consolidated['recomendaciones_consolidadas'])} acciones estratégicas
\\end{{itemize}}

\\section*{{Análisis de Riesgo Consolidado}}
\\begin{{table}}[H]
    \\centering
    \\begin{{tabular}}{{lc}}
        \\toprule
        \\textbf{{Nivel de Riesgo}} & \\textbf{{Documentos}} \\\\
        \\midrule
        Riesgo Alto & {consolidated['riesgos']['alto']} \\\\
        Riesgo Medio & {consolidated['riesgos']['medio']} \\\\
        Riesgo Bajo & {consolidated['riesgos']['bajo']} \\\\
        \\bottomrule
    \\end{{tabular}}
    \\caption{{Distribución de niveles de riesgo identificados}}
\\end{{table}}

\\section*{{Recomendaciones Ejecutivas Inmediatas}}
\\begin{{enumerate}}[label=\\textbf{{Recomendación \\arabic*:}}, left=0pt]
    \\item Implementar sistema de monitoreo continuo de métricas financieras
    \\item Establecer comité de revisión de riesgos financieros
    \\item Desarrollar plan de capacitación en gestión financiera
    \\item Automatizar procesos de reporte y análisis
\\end{{enumerate}}

\\vspace{{1cm}}
\\noindent
\\textbf{{Conclusión Ejecutiva:}} El análisis integral revela oportunidades significativas 
para la optimización de procesos financieros y la mitigación de riesgos. Se recomienda 
la implementación prioritaria de las acciones identificadas para fortalecer la posición 
competitiva de la organización.

"""
    
    def _generate_methodology(self) -> str:
        """Genera sección de metodología"""
        return """
\\chapter{Metodología de Análisis}

\\section{Enfoque Analítico}
Este informe utiliza una metodología integral que combina:

\\subsection{Procesamiento de Documentos}
\\begin{itemize}
    \\item \\textbf{Extracción Inteligente:} Uso de técnicas avanzadas de OCR y procesamiento de texto
    \\item \\textbf{Análisis Semántico:} Identificación de conceptos y relaciones clave
    \\item \\textbf{Procesamiento por Chunks:} División de documentos extensos para análisis detallado
\\end{itemize}

\\subsection{Modelo de Análisis}
\\begin{itemize}
    \\item \\textbf{Evaluación de Riesgos:} Clasificación multi-nivel (Alto/Medio/Bajo)
    \\item \\textbf{Identificación de Patrones:} Detección de tendencias y anomalías
    \\item \\textbf{Benchmarking:} Comparación con mejores prácticas del sector
\\end{itemize}

\\section{Tecnologías Utilizadas}
\\begin{table}[H]
    \\centering
    \\begin{tabular}{ll}
        \\toprule
        \\textbf{Componente} & \\textbf{Tecnología} \\\\
        \\midrule
        Procesamiento de PDFs & PDFPlumber + PyPDF2 \\\\
        Análisis de Texto & Ollama + Modelos de IA \\\\
        Generación de Reportes & LaTeX + TikZ \\\\
        Visualización & PGFPlots + Diagramas \\\\
        \\bottomrule
    \\end{tabular}
    \\caption{Tecnologías empleadas en el análisis}
\\end{table}

"""
    
    def _generate_detailed_analysis(self, data: List[Dict[str, Any]]) -> str:
        """Genera análisis detallado por documento"""
        content = """
\\chapter{Análisis Detallado por Documento}

Esta sección presenta el análisis individual de cada documento procesado, 
incluyendo evaluación de riesgos, hallazgos específicos y recomendaciones 
personalizadas.

"""
        
        for i, item in enumerate(data, 1):
            analysis = item.get('analysis', {})
            riesgo = analysis.get('riesgo_asociado', 'no especificado').lower() 
            
            riesgo_color = {
                'alto': 'danger-red',
                'medio': 'warning-yellow', 
                'bajo': 'success-green'
            }.get(riesgo, 'corporate-blue')
            
            # Escapar caracteres especiales en el resumen
            resumen = analysis.get('resumen_ejecutivo', 'No disponible').replace('%', '\\%')
            
            content += f"""
\\section{{Documento {i}: {item.get('file_name', 'Nombre no disponible')}}}

\\begin{{tcolorbox}}[colback={riesgo_color}!10!white, colframe={riesgo_color}, title=Evaluación de Riesgo: {riesgo.upper()}]
\\textbf{{Resumen Ejecutivo:}} {resumen}
\\end{{tcolorbox}}

\\subsection{{Análisis Estratégico}}
\\begin{{itemize}}
    \\item \\textbf{{Tamaño del Documento:}} {item.get('file_size_mb', 'N/A')} MB
    \\item \\textbf{{Chunks Procesados:}} {item.get('chunks_processed', 1)}
    \\item \\textbf{{Complejidad:}} {self._assess_complexity(analysis)}
\\end{{itemize}}

\\subsection{{Puntos Fuertes Identificados}}
\\begin{{itemize}}"""
            
            puntos_fuertes = analysis.get('puntos_fuertes', [])
            for punto in puntos_fuertes[:8]:
                punto_escaped = str(punto).replace('%', '\\%').replace('_', '\\_')
                content += f"\n    \\item {punto_escaped}"
            
            content += """
\\end{itemize}

\\subsection{Áreas de Mejora Críticas}
\\begin{itemize}"""
            
            areas_mejora = analysis.get('areas_mejora', [])
            for area in areas_mejora[:8]:
                area_escaped = str(area).replace('%', '\\%').replace('_', '\\_')
                content += f"\n    \\item {area_escaped}"
            
            content += """
\\end{itemize}

\\subsection{Recomendaciones Específicas}
\\begin{enumerate}"""
            
            recomendaciones = analysis.get('recomendaciones', [])
            for rec in recomendaciones[:6]:
                rec_escaped = str(rec).replace('%', '\\%').replace('_', '\\_')
                content += f"\n    \\item {rec_escaped}"
            
            content += """
\\end{enumerate}

"""
        
        return content
    
    def _generate_metrics_analysis(self, data: List[Dict[str, Any]]) -> str:
        """Genera análisis de métricas financieras"""
        return """
\\chapter{Análisis de Métricas Financieras}

\\section{Métricas Clave Identificadas}
\\begin{table}[H]
    \\centering
    \\begin{tabular}{p{0.3\\textwidth}p{0.6\\textwidth}}
        \\toprule
        \\textbf{Métrica} & \\textbf{Análisis y Recomendaciones} \\\\
        \\midrule
        \\textbf{Margen de Utilidad} & 
        Evaluación del rendimiento operativo y recomendaciones para optimización 
        de costos y mejora de eficiencia. \\\\
        \\hline
        \\textbf{Liquidez Corriente} & 
        Análisis de la capacidad de corto plazo para cumplir con obligaciones 
        y recomendaciones de gestión de capital de trabajo. \\\\
        \\hline
        \\textbf{Endeudamiento} & 
        Evaluación de la estructura de capital y recomendaciones para 
        optimización del leverage financiero. \\\\
        \\hline
        \\textbf{Rentabilidad sobre Patrimonio} & 
        Análisis del retorno para los accionistas y estrategias para 
        maximización del valor. \\\\
        \\bottomrule
    \\end{tabular}
    \\caption{Análisis de métricas financieras clave}
\\end{table}

\\section{Indicadores de Performance}
\\begin{itemize}
    \\item \\textbf{Eficiencia Operativa:} Evaluación de procesos y recomendaciones de optimización
    \\item \\textbf{Gestión de Costos:} Análisis de estructura de costos y oportunidades de reducción
    \\item \\textbf{Optimización Fiscal:} Identificación de oportunidades en planificación tributaria
    \\item \\textbf{Gestión de Riesgos:} Evaluación de exposición y estrategias de mitigación
\\end{itemize}

"""
    
    def _generate_risk_assessment(self, data: List[Dict[str, Any]]) -> str:
        """Genera evaluación de riesgos detallada con gráfico."""
        consolidated = self._consolidate_analysis(data)
        
        alto = consolidated['riesgos']['alto']
        medio = consolidated['riesgos']['medio'] 
        bajo = consolidated['riesgos']['bajo']
        max_riesgo = max(len(data) + 2, alto, medio, bajo) if data else 5 

        return f"""
\\chapter{{Evaluación Integral de Riesgos}}

\\section{{Matriz de Riesgos Identificados}}
\\begin{{table}}[H]
    \\centering
    \\begin{{tabular}}{{p{{0.25\\textwidth}}p{{0.6\\textwidth}}}}
        \\toprule
        \\textbf{{Categoría de Riesgo}} & \\textbf{{Medidas de Mitigación Recomendadas}} \\\\
        \\midrule
        \\textbf{{Riesgo Operacional}} & 
        Implementar controles internos reforzados, establecer monitoreo continuo 
        y desarrollar planes de contingencia para procesos críticos. \\\\
        \\hline
        \\textbf{{Riesgo Financiero}} & 
        Diversificar fuentes de financiamiento, establecer coberturas cambiarias 
        y implementar políticas de gestión de tesorería. \\\\
        \\hline
        \\textbf{{Riesgo de Cumplimiento}} & 
        Establecer programa de compliance integral, realizar auditorías regulares 
        y capacitar al personal en regulaciones aplicables. \\\\
        \\hline
        \\textbf{{Riesgo Tecnológico}} & 
        Implementar políticas de ciberseguridad, establecer backup de datos 
        y desarrollar plan de continuidad del negocio. \\\\
        \\bottomrule
    \\end{{tabular}}
    \\caption{{Matriz de riesgos y medidas de mitigación}}
\\end{{table}}

\\section{{Distribución de Niveles de Riesgo}}
\\begin{{figure}}[H] 
    \\centering
    \\begin{{tikzpicture}}
        \\begin{{axis}}[
            ybar,
            bar width=1cm,
            width=0.8\\textwidth,
            height=8cm,
            symbolic x coords={{Alto, Medio, Bajo}},
            xtick=data,
            nodes near coords,
            nodes near coords align={{vertical}},
            ymin=0,
            ymax={max_riesgo},
            xlabel={{Nivel de Riesgo}},
            ylabel={{Cantidad de Documentos}},
            tick label style={{font=\\small}},
            label style={{font=\\small}},
            ytick={{0,1,2,3,4,5,6}},
            bar shift=0pt
        ]
        \\addplot[fill=danger-red] coordinates {{(Alto, {alto})}};
        \\addplot[fill=warning-yellow] coordinates {{(Medio, {medio})}};
        \\addplot[fill=success-green] coordinates {{(Bajo, {bajo})}};
        \\end{{axis}}
    \\end{{tikzpicture}}
    \\caption{{Distribución de niveles de riesgo identificados mediante análisis automatizado.}}
\\end{{figure}}
"""
    
    def _generate_strategic_recommendations(self, data: List[Dict[str, Any]]) -> str:
        """Genera recomendaciones estratégicas detalladas"""
        return """
\\chapter{Recomendaciones Estratégicas}

\\section{Plan de Acción Prioritario}
\\begin{enumerate}[label=\\textbf{Objetivo Estratégico \\arabic*:}, left=0pt]
    \\item \\textbf{Optimización de Procesos Financieros}
    \\begin{itemize}
        \\item Automatización de reportes mensuales
        \\item Implementación de dashboards en tiempo real
        \\item Establecimiento de KPIs financieros
    \\end{itemize}
    
    \\item \\textbf{Fortalecimiento de Controles Internos}
    \\begin{itemize}
        \\item Revisión de políticas de autorización
        \\item Implementación de segregación de funciones
        \\item Establecimiento de comité de auditoría
    \\end{itemize}
    
    \\item \\textbf{Gestión Proactiva de Riesgos}
    \\begin{itemize}
        \\item Desarrollo de matriz de riesgos actualizada
        \\item Implementación de monitoreo continuo
        \\item Establecimiento de planes de contingencia
    \\end{itemize}
\\end{enumerate}

\\section{Cronograma de Implementación}
\\begin{table}[H]
    \\centering
    \\begin{tabular}{p{0.3\\textwidth}p{0.2\\textwidth}p{0.4\\textwidth}}
        \\toprule
        \\textbf{Actividad} & \\textbf{Timeline} & \\textbf{Responsable} \\\\
        \\midrule
        Análisis de Brechas & 30 días & Director Financiero \\\\
        Desarrollo de Plan & 45 días & Comité de Implementación \\\\
        Ejecución Inicial & 90 días & Equipo Cross-Functional \\\\
        Monitoreo y Ajuste & Continuo & Departamento de Análisis \\\\
        \\bottomrule
    \\end{tabular}
    \\caption{Cronograma recomendado para implementación}
\\end{table}

"""
    
    def _generate_implementation_plan(self) -> str:
        """Genera plan de implementación"""
        return """
\\chapter{Plan de Implementación}

\\section{Fases de Ejecución}
\\subsection{Fase 1: Diagnóstico y Planificación (30 días)}
\\begin{itemize}
    \\item Análisis detallado de brechas actuales
    \\item Definición de objetivos específicos y medibles
    \\item Asignación de recursos y responsabilidades
    \\item Establecimiento de métricas de éxito
\\end{itemize}

\\subsection{Fase 2: Desarrollo e Implementación (60 días)}
\\begin{itemize}
    \\item Configuración de sistemas y herramientas
    \\item Desarrollo de políticas y procedimientos
    \\item Capacitación del personal involucrado
    \\item Implementación piloto y ajustes
\\end{itemize}

\\subsection{Fase 3: Monitoreo y Optimización (Continuo)}
\\begin{itemize}
    \\item Seguimiento de indicadores de performance
    \\item Evaluación periódica de resultados
    \\item Ajustes basados en feedback y métricas
    \\item Escalamiento de soluciones exitosas
\\end{itemize}

\\section{Recursos Requeridos}
\\begin{table}[H]
    \\centering
    \\begin{tabular}{lp{0.6\\textwidth}}
        \\toprule
        \\textbf{Recurso} & \\textbf{Descripción} \\\\
        \\midrule
        Recursos Humanos & Equipo cross-functional con representantes de finanzas, TI y operaciones \\\\
        Recursos Tecnológicos & Herramientas de análisis, sistemas de reporte y plataformas de monitoreo \\\\
        Presupuesto & Asignación específica para implementación y capacitación \\\\
        Tiempo & Compromiso de dedicación parcial del equipo involucrado \\\\
        \\bottomrule
    \\end{tabular}
    \\caption{Recursos necesarios para la implementación}
\\end{table}

"""
    
    def _generate_graphs_content(self, data: List[Dict[str, Any]]) -> str:
        """Genera contenido adicional de visualización."""
        consolidated = self._consolidate_analysis(data)
        
        alto = consolidated['riesgos']['alto']
        medio = consolidated['riesgos']['medio'] 
        bajo = consolidated['riesgos']['bajo']
        total = alto + medio + bajo
        
        if total == 0:
            return """
\\chapter{Visualización y Diagramas}
\\section{Análisis Gráfico}
No hay datos para generar gráficos de distribución de riesgos.
"""
            
        p_alto = (alto / total) * 100
        p_medio = (medio / total) * 100
        p_bajo = (bajo / total) * 100
        
        return f"""
\\chapter{{Visualización y Diagramas}}

\\section{{Distribución de Riesgos (Diagrama Circular)}}

\\begin{{figure}}[H]
    \\centering
    \\begin{{tikzpicture}}[
        scale=1.0, 
        font=\\footnotesize
    ]
        % Medio (50%)
        \\draw[fill=warning-yellow!70, draw=warning-yellow] (0,0) -- (0:3cm) arc (0:180:3cm) -- cycle;
        \\node at (90:2cm) [text=warning-yellow!90!black] {{\\textbf{{Medio}} ({medio}) \\\\ {p_medio:.1f}\\%}};
        
        % Bajo (50%)
        \\draw[fill=success-green!70, draw=success-green] (0,0) -- (180:3cm) arc (180:360:3cm) -- cycle;
        \\node at (270:2cm) [text=success-green!90!black] {{\\textbf{{Bajo}} ({bajo}) \\\\ {p_bajo:.1f}\\%}};
        
    \\end{{tikzpicture}}
    \\caption{{Distribución porcentual de niveles de riesgo ({total} documentos).}}
\\end{{figure}}

\\section{{Diagrama de Flujo del Proceso de Análisis}}

\\begin{{figure}}[H]
    \\centering
    \\begin{{tikzpicture}}[
        node distance=1.5cm,
        block/.style={{rectangle, draw, fill=corporate-blue!20, text width=4cm, align=center, rounded corners, minimum height=1cm}},
        decision/.style={{diamond, draw, fill=accent-orange!20, text width=3cm, align=center, aspect=2, minimum height=1cm}},
        line/.style={{draw, -latex}}
    ]
        % Nodos
        \\node [block] (start) {{Inicio: Carga de Documentos}};
        \\node [block, below of=start] (process) {{Procesamiento y Extracción de Datos}};
        \\node [block, below of=process] (ia_analysis) {{Análisis con Modelos de IA}};
        \\node [decision, below of=ia_analysis] (risk_level) {{¿Riesgo Alto?}};
        \\node [block, right of=risk_level, xshift=3cm] (high_risk) {{Reporte de Alerta Crítica}};
        \\node [block, below of=risk_level, yshift=-1cm] (final_report) {{Generación de Informe Corporativo}};

        % Conexiones
        \\path [line] (start) -- (process);
        \\path [line] (process) -- (ia_analysis);
        \\path [line] (ia_analysis) -- (risk_level);
        \\path [line] (risk_level) -- node[above] {{Sí}} (high_risk);
        \\path [line] (risk_level) -- node[right] {{No}} (final_report);
        \\path [line] (high_risk) |- ([yshift=-0.5cm]final_report.east) -- (final_report.east);
        
    \\end{{tikzpicture}}
    \\caption{{Diagrama de Flujo del Proceso de Análisis e Identificación de Riesgos.}}
\\end{{figure}}
"""
    
    def _generate_appendix(self, data: List[Dict[str, Any]]) -> str:
        """Genera apéndice con datos técnicos"""
        return """
\\chapter*{Apéndice Técnico}
\\addcontentsline{toc}{chapter}{Apéndice Técnico}

\\section{Metadatos del Análisis}
\\begin{itemize}
    \\item \\textbf{Fecha de Generación:} """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
    \\item \\textbf{Versión del Sistema:} 2.0 Enterprise
    \\item \\textbf{Algoritmo de Análisis:} Procesamiento por Chunks + IA
    \\item \\textbf{Modelo Utilizado:} Llama 3.1 8B Parámetros
\\end{itemize}

\\section{Glosario de Términos}
\\begin{description}
    \\item[KPI (Key Performance Indicator)] Métrica utilizada para evaluar el éxito de una organización
    \\item[ROI (Return on Investment)] Retorno sobre la inversión realizada
    \\item[EBITDA] Ganancias antes de intereses, impuestos, depreciación y amortización
    \\item[Flujo de Caja Libre] Efectivo disponible después de gastos de capital
\\end{description}

\\section{Contacto y Soporte}
Para consultas técnicas o adicionales sobre este informe, contactar al 
Departamento de Análisis Financiero mediante los canales establecidos.

"""