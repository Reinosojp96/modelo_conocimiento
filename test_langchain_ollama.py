from langchain_community.llms import Ollama

# Crear instancia del modelo
llm = Ollama(model="llama3")

# Probar en español
prompt = "Explícame brevemente qué es el aprendizaje profundo en lenguaje natural."
respuesta = llm.invoke(prompt)

print("🤖 Respuesta del modelo:\n", respuesta)
