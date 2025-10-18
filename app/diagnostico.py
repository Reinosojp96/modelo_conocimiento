import ollama

print("=== DIAGNÓSTICO OLLAMA ===")
print("1. Probando conexión...")

try:
    result = ollama.list()
    print("✓ Conexión exitosa")
    print(f"Tipo de respuesta: {type(result)}")
    print(f"Respuesta completa: {result}")
    
    print("\n2. Analizando estructura...")
    if isinstance(result, dict):
        print("Es un diccionario")
        print(f"Claves: {list(result.keys())}")
        if 'models' in result:
            print(f"Modelos: {result['models']}")
    else:
        print("No es un diccionario")
        print(f"Longitud: {len(result) if hasattr(result, '__len__') else 'No tiene longitud'}")
        
except Exception as e:
    print(f"✗ Error: {e}")