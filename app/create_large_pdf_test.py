# create_large_pdf_test.py
from fpdf import FPDF
import os

def create_enterprise_test_pdf():
    """Crea un PDF empresarial de prueba grande"""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Encabezado corporativo
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, 'INFORME FINANCIERO CORPORATIVO 2024', 0, 1, 'C')
    pdf.ln(10)
    
    # Contenido masivo
    sections = [
        "ESTADO DE SITUACIÓN FINANCIERA",
        "ESTADO DE RESULTADOS INTEGRALES", 
        "ESTADO DE FLUJOS DE EFECTIVO",
        "NOTAS A LOS ESTADOS FINANCIEROS",
        "ANÁLISIS DE MARGEN DE CONTRIBUCIÓN",
        "PROYECCIONES FINANCIERAS",
        "ANÁLISIS DE SENSIBILIDAD",
        "EVALUACIÓN DE RIESGOS",
        "CONTROLES INTERNOS",
        "COMPLIANCE Y REGULATORIO"
    ]
    
    for i, section in enumerate(sections):
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(200, 10, f'{i+1}. {section}', 0, 1)
        pdf.ln(5)
        
        # Contenido detallado de cada sección
        pdf.set_font('Arial', '', 12)
        for j in range(5):  # 5 páginas por sección
            content = f"""
            Esta es la página {j+1} de la sección {section}. Contiene análisis financiero detallado 
            sobre métricas clave de rendimiento, ratios de liquidez, indicadores de solvencia y 
            proyecciones estratégicas para el próximo ejercicio fiscal.
            
            Los principales hallazgos incluyen un crecimiento orgánico del 15% en ingresos, 
            una mejora del margen EBITDA del 2.3%, y una reducción del costo de capital del 1.8%. 
            Se identificaron oportunidades de optimización en la cadena de suministro que podrían 
            generar ahorros adicionales por aproximadamente $2.5 millones anuales.
            
            El análisis de sensibilidad indica que un cambio del 10% en los tipos de cambio 
            impactaría los resultados en aproximadamente $4.2 millones. Se recomienda implementar 
            coberturas cambiarias para mitigar este riesgo exposure.
            
            En términos de gobernanza, se detectaron 3 áreas de mejora en los controles internos 
            relacionadas con la segregación de funciones en el proceso de aprobación de gastos. 
            Se sugiere revisar y actualizar las políticas de autorización para alinearlas con 
            las mejores prácticas del sector.
            """
            
            pdf.multi_cell(0, 10, content)
            if j < 4:  # No añadir página después del último contenido
                pdf.add_page()
    
    # Guardar
    output_path = "../input_pdfs/informe_corporativo_masivo.pdf"
    pdf.output(output_path)
    print(f"✅ PDF creado: {output_path}")
    print(f"📊 Aproximadamente 50+ páginas de contenido empresarial")

if __name__ == "__main__":
    create_enterprise_test_pdf()