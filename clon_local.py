import ollama

# Usamos el modelo que acabas de compilar
NOMBRE_MODELO = "mi_clon_m4"

# Memoria del chat
historial_mensajes = []

def consultar_clon_local(mensaje_usuario):
    # Guardamos tu orden en la memoria
    historial_mensajes.append({'role': 'user', 'content': mensaje_usuario})
    
    try:
        # Llamada 100% local a Ollama
        respuesta = ollama.chat(model=NOMBRE_MODELO, messages=historial_mensajes)
        contenido_respuesta = respuesta['message']['content']
        
        # Guardamos la respuesta para mantener el contexto
        historial_mensajes.append({'role': 'assistant', 'content': contenido_respuesta})
        return contenido_respuesta
        
    except Exception as e:
        return f"Error en conexión local: {e}"

if __name__ == "__main__":
    print(f"--- Clon Digital LOCAL Activado ({NOMBRE_MODELO}) ---")
    print("Estado: Offline / M4 Pro / Obediencia Absoluta")
    print("(Escribe 'salir' para terminar)\n")
    
    while True:
        texto_usuario = input("Tú: ")
        
        if texto_usuario.lower() == "salir":
            print("Apagando sistema local.")
            break
            
        if not texto_usuario.strip():
            continue
            
        resultado = consultar_clon_local(texto_usuario)
        print(f"\nClon: {resultado}\n")