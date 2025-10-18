# agente_local.py
# Compatible con langchain-core 1.x y langchain-community 0.4.x

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser


# Memoria de conversación simple
class MemoriaConversacion:
    def __init__(self):
        self.mensajes = []

    def agregar(self, rol, contenido):
        self.mensajes.append((rol, contenido))

    def obtener_historial(self):
        historial = ""
        for rol, contenido in self.mensajes[-10:]:  # guarda las últimas 10 interacciones
            historial += f"{rol}: {contenido}\n"
        return historial


# 1️⃣ Modelo local de Ollama
llm = ChatOllama(model="llama3", temperature=0.7)

# 2️⃣ Plantilla del prompt
prompt = ChatPromptTemplate.from_template("""
Eres un asistente que razona y responde en español.
Usa el contexto previo para mantener coherencia en la conversación.

Historial:
{history}
Usuario: {input}
Asistente:
""")

# 3️⃣ Inicializa memoria y parser
memoria = MemoriaConversacion()
parser = StrOutputParser()


# 4️⃣ Bucle principal
def ejecutar_agente():
    print("🤖 Agente local con Ollama iniciado. Escribe 'salir' para terminar.\n")

    while True:
        entrada = input("Tú: ").strip()
        if entrada.lower() in ["salir", "exit", "quit"]:
            print("👋 Hasta luego.")
            break

        memoria.agregar("Usuario", entrada)
        historial = memoria.obtener_historial()

        # Crea el mensaje formateado
        cadena = prompt.format(history=historial, input=entrada)

        # Llama al modelo
        respuesta = llm.invoke(cadena)
        salida = parser.invoke(respuesta)

        print(f"Agente: {salida}\n")

        memoria.agregar("Asistente", salida)


if __name__ == "__main__":
    ejecutar_agente()
