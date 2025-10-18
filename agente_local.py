# agente_local.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory

# 1️⃣ Inicializa el modelo local (asegúrate de tener uno descargado, como 'mistral' o 'llama3')
llm = ChatOllama(model="llama3", temperature=0.7)

# 2️⃣ Crea la plantilla del prompt
prompt = ChatPromptTemplate.from_template("""
Eres un agente inteligente que razona en español.
Responde de forma clara y profesional a lo que el usuario diga.
Historial de conversación:
{history}
Usuario: {input}
Asistente:
""")

# 3️⃣ Memoria de conversación
memory = ConversationBufferMemory(return_messages=True)

# 4️⃣ Motor de parsing de salida (simple texto)
parser = StrOutputParser()

# 5️⃣ Bucle de interacción
def ejecutar_agente():
    print("🤖 Agente iniciado. Escribe 'salir' para terminar.")
    while True:
        entrada = input("Tú: ")
        if entrada.lower() in ["salir", "exit", "quit"]:
            break

        # Guarda entrada en memoria
        memory.chat_memory.add_user_message(entrada)

        # Genera respuesta
        historial = "\n".join(
            [f"{m.type}: {m.content}" for m in memory.chat_memory.messages]
        )
        cadena = prompt.format(history=historial, input=entrada)
        respuesta = llm.invoke(cadena)
        print("Agente:", respuesta.content)

        # Guarda respuesta
        memory.chat_memory.add_ai_message(respuesta.content)


if __name__ == "__main__":
    ejecutar_agente()
