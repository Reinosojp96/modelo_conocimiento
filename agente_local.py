from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
import uvicorn

# Inicializa el modelo de Ollama
model = OllamaLLM(model="llama3")

# Inicializa la API
app = FastAPI(title="Agente Local con Ollama")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/query")
def query_agent(data: PromptRequest):
    """
    Endpoint que recibe un prompt y devuelve la respuesta generada por el modelo.
    """
    try:
        response = model.invoke(data.prompt)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("🚀 Servidor del agente local iniciado en http://localhost:8000/query")
    uvicorn.run(app, host="0.0.0.0", port=8000)
