from typing import List, Dict, Any
from datetime import datetime
import json

class LatexGenerator:
    def __init__(self):
        pass
    
    def generate_corporate_report(self, data: List[Dict[str, Any]], output_path: str) -> str:
        """Genera un documento LaTeX profesional corporativo"""
        try:
            latex_content = self._create_latex_document(data)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            return output_path
        except Exception as e:
            print(f"Error generando reporte LaTeX: {e}")
            raise
    
    def _create_latex_document(self, data: List[Dict[str, Any]]) -> str:
        """Crea el contenido completo del documento LaTeX"""
        
        main_content = self._generate_main_content(data)
        graphs_content = self._generate_graphs_content(data)
        current_date = datetime.now().strftime('%d de %B de %Y')
        num_docs = len(data)
        
        latex_template = f"""\\documentclass[11pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[spanish]{{babel}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=2.5cm}}
\\usepackage{{graphicx}}
\\usepackage{{tikz}}
\\usepackage{{pgfplots}}
\\usetikzlibrary{{shapes, arrows, positioning, fit}}
\\usepackage{{xcolor}}
\\usepackage{{hyperref}}
\\usepackage{{booktabs}}
\\usepackage{{array}}
\\usepackage{{float}}

% Colores corporativos
\\definecolor{{corporate-blue}}{{RGB}}{{0, 82, 155}}
\\definecolor{{corporate-gray}}{{RGB}}{{240, 240, 240}}
\\definecolor{{accent-orange}}{{RGB}}{{255, 102, 0}}

% Estilo profesional
\\usepackage{{titlesec}}
\\titleformat{{\\section}}{{\\color{{corporate-blue}}\\normalfont\\Large\\bfseries}}{{}}{{0pt}}{{}}
\\titleformat{{\\subsection}}{{\\color{{corporate-blue}}\\normalfont\\large\\bfseries}}{{}}{{0pt}}{{}}

\\usepackage{{fancyhdr}}
\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyhead[L]{{\\textcolor{{corporate-blue}}{{\\footnotesize Análisis Financiero Corporativo}}}}
\\fancyhead[R]{{\\textcolor{{corporate-blue}}{{\\footnotesize \\thepage}}}}
\\renewcommand{{\\headrulewidth}}{{0.4pt}}
\\renewcommand{{\\headrule}}{{\\color{{corporate-blue}}\\hrule}}

\\begin{{document}}

% Portada corporativa
\\begin{{titlepage}}
    \\centering
    \\vspace*{{2cm}}
    % \\includegraphics[width=0.3\\textwidth]{{logo_empresa.png}} % Reemplazar con logo real
    \\vspace{{1cm}}
    
    {{\\Huge\\color{{corporate-blue}}\\textbf{{ANÁLISIS FINANCIERO CORPORATIVO}}}}
    \\vspace{{1cm}}
    
    {{\\Large\\textbf{{Informe de Diagnóstico Integral}}}}
    \\vspace{{1.5cm}}
    
    {{\\large Generado el: {current_date}}}
    \\vspace{{0.5cm}}
    
    {{\\large Documentos analizados: {num_docs}}}
    \\vspace{{2cm}}
    
    \\rule{{\\textwidth}}{{0.4pt}}
    \\vspace{{0.5cm}}
    
    {{\\large Departamento de Análisis Financiero}}
    \\vfill
\\end{{titlepage}}

% Tabla de contenidos
\\tableofcontents
\\newpage

{main_content}

% Sección de Grafos y Diagramas
\\section{{Análisis Gráfico y Diagramas}}
{graphs_content}

\\end{{document}}"""
        return latex_template
    
    def _generate_main_content(self, data: List[Dict[str, Any]]) -> str:
        """Genera el contenido principal del documento"""
        
        consolidated = self._consolidate_analysis(data)
        
        content = f"""
    % Resumen Ejecutivo
    \\section{{Resumen Ejecutivo}}
    \\noindent\\fbox{{\\parbox{{\\textwidth}}{{
    {consolidated['resumen_ejecutivo']}
    }}}}

    % Análisis por Documento
    \\section{{Análisis por Documento}}
    """
        
        for item in data:
            analysis = item.get('analysis', {})  # CORRECCIÓN: {} en lugar de {{}}
            resumen = analysis.get('resumen_ejecutivo', 'No disponible')
            riesgo = analysis.get('riesgo_asociado', 'No especificado')
            
            content += f"""
    \\subsection{{{item['file_name']}}}
    \\textbf{{Resumen:}} {resumen}

    \\textbf{{Riesgo:}} {riesgo}

    \\subsubsection{{Puntos Fuertes}}
    \\begin{{itemize}}
    """
            # Manejar diferentes tipos de datos en puntos_fuertes
            puntos_fuertes = analysis.get('puntos_fuertes', [])
            if isinstance(puntos_fuertes, list):
                for punto in puntos_fuertes[:5]:  # Limitar a 5 puntos
                    if isinstance(punto, str):
                        content += f"    \\item {punto}\n"
                    else:
                        content += f"    \\item {str(punto)}\n"
            
            content += """\\end{itemize}

    \\subsubsection{Áreas de Mejora}
    \\begin{itemize}
    """
            areas_mejora = analysis.get('areas_mejora', [])
            if isinstance(areas_mejora, list):
                for area in areas_mejora[:5]:  # Limitar a 5 áreas
                    if isinstance(area, str):
                        content += f"    \\item {area}\n"
                    else:
                        content += f"    \\item {str(area)}\n"
            
            content += """\\end{itemize}

    \\subsubsection{Recomendaciones}
    \\begin{itemize}
    """
            recomendaciones = analysis.get('recomendaciones', [])
            if isinstance(recomendaciones, list):
                for rec in recomendaciones[:5]:  # Limitar a 5 recomendaciones
                    if isinstance(rec, str):
                        content += f"    \\item {rec}\n"
                    else:
                        content += f"    \\item {str(rec)}\n"
            
            content += "\\end{itemize}\n\n"
        
        return content
    
    def _generate_graphs_content(self, data: List[Dict[str, Any]]) -> str:
        """Genera el contenido con todos los grafos y diagramas"""
        
        consolidated = self._consolidate_analysis(data)
        alto = consolidated['riesgos']['alto']
        medio = consolidated['riesgos']['medio'] 
        bajo = consolidated['riesgos']['bajo']
        max_riesgo = len(data) + 2
        
        graphs = f"""
% Gráfico de Riesgos
\\subsection{{Distribución de Riesgos}}
\\begin{{figure}}[H]
    \\centering
    \\begin{{tikzpicture}}
        \\begin{{axis}}[
            ybar,
            bar width=0.8cm,
            width=0.8\\textwidth,
            height=6cm,
            symbolic x coords={{Alto, Medio, Bajo}},
            xtick=data,
            nodes near coords,
            nodes near coords align={{vertical}},
            ymin=0,
            ymax={max_riesgo},
            xlabel={{Nivel de Riesgo}},
            ylabel={{Cantidad de Documentos}},
            tick label style={{font=\\small}},
            label style={{font=\\small}}
        ]
        \\addplot[fill=corporate-blue] coordinates {{(Alto, {alto}) (Medio, {medio}) (Bajo, {bajo})}};
        \\end{{axis}}
    \\end{{tikzpicture}}
    \\caption{{Distribución de niveles de riesgo identificados}}
\\end{{figure}}

% Diagrama de Flujo de Procesos
\\subsection{{Diagrama de Procesos Identificados}}
{self._generate_process_diagram()}

% Grafo de Relaciones Departamentales  
\\subsection{{Mapa de Relaciones Organizacionales}}
{self._generate_relationship_graph()}

% Mapa Conceptual de Términos
\\subsection{{Mapa Conceptual Financiero}}
{self._generate_concept_map()}

% Arquitectura Organizacional
\\subsection{{Diagrama de Arquitectura Organizacional}}
{self._generate_org_architecture()}
"""
        return graphs
    
    def _generate_process_diagram(self) -> str:
        """Genera diagrama de flujo de procesos"""
        return """
\\begin{figure}[H]
    \\centering
    \\begin{tikzpicture}[node distance=2cm, auto]
        \\tikzstyle{process} = [rectangle, draw=corporate-blue, fill=corporate-gray, thick, minimum width=3cm, minimum height=1cm, text centered, rounded corners]
        \\tikzstyle{decision} = [diamond, draw=accent-orange, fill=orange!20, thick, minimum width=2cm, minimum height=1cm, text centered, aspect=2]
        \\tikzstyle{arrow} = [thick,->,>=stealth]
        
        \\node (start) [process] {Inicio del Proceso};
        \\node (analysis) [process, below of=start] {Análisis Financiero};
        \\node (decision) [decision, below of=analysis] {¿Riesgo Alto?};
        \\node (action1) [process, right of=decision, xshift=3cm] {Acción Correctiva};
        \\node (action2) [process, below of=decision, yshift=-1cm] {Seguimiento Normal};
        \\node (end) [process, below of=action2] {Finalización};
        
        \\draw [arrow] (start) -- (analysis);
        \\draw [arrow] (analysis) -- (decision);
        \\draw [arrow] (decision) -- node[near start] {Sí} (action1);
        \\draw [arrow] (decision) -- node[near start] {No} (action2);
        \\draw [arrow] (action1) |- (end);
        \\draw [arrow] (action2) -- (end);
    \\end{tikzpicture}
    \\caption{Diagrama de flujo del proceso de análisis financiero}
\\end{figure}
"""
    
    def _generate_relationship_graph(self) -> str:
        """Genera grafo de relaciones departamentales"""
        return """
\\begin{figure}[H]
    \\centering
    \\begin{tikzpicture}[
        node distance=3cm,
        department/.style={rectangle, draw=corporate-blue, fill=corporate-gray, thick, minimum width=2.5cm, minimum height=1cm, text centered, rounded corners},
        relation/.style={->, thick, >=stealth}
    ]
    
        \\node[department] (finance) {Finanzas};
        \\node[department, right of=finance] (operations) {Operaciones};
        \\node[department, below of=finance] (sales) {Ventas};
        \\node[department, right of=sales] (marketing) {Marketing};
        
        \\draw[relation] (sales) -- node[midway, left] {Informes} (finance);
        \\draw[relation] (operations) -- node[midway, above] {Costos} (finance);
        \\draw[relation] (marketing) -- node[midway, right] {Presupuesto} (finance);
        \\draw[relation] (sales) -- node[midway, below] {Coordinación} (operations);
        
    \\end{tikzpicture}
    \\caption{Mapa de relaciones interdepartamentales identificadas}
\\end{figure}
"""
    
    def _generate_concept_map(self) -> str:
        """Genera mapa conceptual de términos financieros"""
        return """
\\begin{figure}[H]
    \\centering
    \\begin{tikzpicture}[
        concept/.style={ellipse, draw=accent-orange, fill=orange!20, thick, minimum width=2cm, minimum height=1cm, text centered},
        connection/.style={->, thick, >=stealth, bend left=15}
    ]
    
        \\node[concept] (income) {Ingresos};
        \\node[concept, right of=income, xshift=3cm] (costs) {Costos};
        \\node[concept, below of=income, yshift=-1cm] (profit) {Utilidades};
        \\node[concept, right of=profit, xshift=3cm] (cashflow) {Flujo de Caja};
        
        \\draw[connection] (income) to node[midway, above] {Genera} (profit);
        \\draw[connection] (costs) to node[midway, above] {Afecta} (profit);
        \\draw[connection] (profit) to node[midway, right] {Impacta} (cashflow);
        \\draw[connection] (income) to node[midway, left] {Financia} (cashflow);
        
    \\end{tikzpicture}
    \\caption{Mapa conceptual de términos financieros clave}
\\end{figure}
"""
    
    def _generate_org_architecture(self) -> str:
        """Genera diagrama de arquitectura organizacional"""
        return """
\\begin{figure}[H]
    \\centering
    \\begin{tikzpicture}[
        level 1/.style={sibling distance=4cm},
        level 2/.style={sibling distance=2cm},
        every node/.style={rectangle, draw=corporate-blue, fill=corporate-gray, thick, minimum width=2.5cm, text centered, rounded corners}
    ]
    
    \\node {Gerencia General}
        child {node {Finanzas}
            child {node {Contabilidad}}
            child {node {Análisis}}
        }
        child {node {Operaciones}
            child {node {Producción}}
            child {node {Logística}}
        }
        child {node {Comercial}
            child {node {Ventas}}
            child {node {Marketing}}
        };
    
    \\end{tikzpicture}
    \\caption{Arquitectura organizacional sugerida}
\\end{figure}
"""
    
    def _consolidate_analysis(self, data: List[Dict[str, Any]]) -> Dict:
        """Consolida el análisis de todos los documentos"""
        riesgos = {'alto': 0, 'medio': 0, 'bajo': 0}
        all_strengths = []
        all_improvements = []
        all_recommendations = []
        
        for item in data:
            analysis = item.get('analysis', {})
            riesgo = analysis.get('riesgo_asociado', 'medio')
            riesgos[riesgo] += 1
            
            # Solo procesar listas de strings, ignorar diccionarios y otros tipos
            puntos_fuertes = analysis.get('puntos_fuertes', [])
            if isinstance(puntos_fuertes, list):
                for punto in puntos_fuertes:
                    if isinstance(punto, str):
                        all_strengths.append(punto)
            
            areas_mejora = analysis.get('areas_mejora', [])
            if isinstance(areas_mejora, list):
                for area in areas_mejora:
                    if isinstance(area, str):
                        all_improvements.append(area)
            
            recomendaciones = analysis.get('recomendaciones', [])
            if isinstance(recomendaciones, list):
                for rec in recomendaciones:
                    if isinstance(rec, str):
                        all_recommendations.append(rec)
        
        # Crear listas únicas usando sets (solo con strings)
        unique_strengths = list(set(all_strengths))[:5]
        unique_improvements = list(set(all_improvements))[:5]
        unique_recommendations = list(set(all_recommendations))[:5]
        
        return {
            'resumen_ejecutivo': f"Análisis consolidado de {len(data)} documentos financieros. Se identificaron {len(unique_strengths)} puntos fuertes principales y {len(unique_improvements)} áreas críticas de mejora.",
            'riesgos': riesgos,
            'puntos_fuertes_consolidados': unique_strengths,
            'areas_mejora_consolidadas': unique_improvements,
            'recomendaciones_consolidadas': unique_recommendations
        }