from langchain_ollama import OllamaLLM

# Usa el modelo que tengas instalado (por ejemplo llama3)
llm = OllamaLLM(model="llama3")

respuesta = llm.invoke("Explica en una frase qué es LangChain.")
print(respuesta)
