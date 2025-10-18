# debug_latex.py
import json
from latex_generator import LatexGenerator

def test_latex_generator():
    print("=== DIAGNÓSTICO LATEX GENERATOR ===")
    
    # Cargar los datos existentes para ver su estructura
    try:
        with open('output/datos_completos.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✓ Datos cargados correctamente")
        print(f"Número de documentos: {len(data)}")
    except Exception as e:
        print(f"✗ Error cargando datos: {e}")
        return
    
    # Inspeccionar la estructura de los datos
    print("\n=== ESTRUCTURA DE DATOS ===")
    for i, item in enumerate(data):
        print(f"\nDocumento {i+1}: {item['file_name']}")
        analysis = item.get('analysis', {})
        print(f"  - Claves en analysis: {list(analysis.keys())}")
        
        # Verificar tipos de datos en listas problemáticas
        for key in ['puntos_fuertes', 'areas_mejora', 'recomendaciones']:
            if key in analysis:
                value = analysis[key]
                print(f"  - {key}: tipo={type(value)}, valor={value}")
                if isinstance(value, list):
                    for j, elem in enumerate(value[:3]):  # Mostrar primeros 3 elementos
                        print(f"    - Elemento {j}: tipo={type(elem)}, valor={elem}")
    
    # Probar la consolidación
    print("\n=== PROBANDO CONSOLIDACIÓN ===")
    try:
        generator = LatexGenerator()
        consolidated = generator._consolidate_analysis(data)
        print("✓ Consolidación exitosa")
        print(f"Resumen: {consolidated['resumen_ejecutivo']}")
    except Exception as e:
        print(f"✗ Error en consolidación: {e}")
        import traceback
        traceback.print_exc()
    
    # Probar generación LaTeX
    print("\n=== PROBANDO GENERACIÓN LATEX ===")
    try:
        generator = LatexGenerator()
        result = generator.generate_corporate_report(data, 'output/test_diagnostico.tex')
        print(f"✓ Generación LaTeX exitosa: {result}")
    except Exception as e:
        print(f"✗ Error en generación LaTeX: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_latex_generator()