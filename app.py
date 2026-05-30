import streamlit as st
import ollama
import PyPDF2

# 1. Configuración de la interfaz (Nota el nuevo título V2.0)
st.set_page_config(page_title="Terminal PCO - Clon Digital", page_icon="⚙️", layout="wide")
st.title("Clon Digital // Interfaz M4 Pro (Versión 2.0)")
st.caption("Estado: Local | Módulos: Texto, Visión & Lectura de Documentos")

MODELO_TEXTO = "mi_clon_m4"
MODELO_VISION = "mi_clon_vision"

# 2. Barra lateral para los "Sentidos" de la IA (AQUÍ ESTÁN LAS CAJAS DE SUBIDA)
with st.sidebar:
    st.header("Módulos de Entrada 📥")
    
    st.subheader("1. Módulo de Visión 👁️")
    imagen_subida = st.file_uploader("Sube imágenes aquí (JPG/PNG)", type=["png", "jpg", "jpeg"])
    
    st.subheader("2. Módulo de Lectura 📄")
    documento_subido = st.file_uploader("Sube documentos aquí (PDF/TXT)", type=["pdf", "txt"])

# 3. Inicializar la memoria
if "historial" not in st.session_state:
    st.session_state.historial = []

# 4. Función interna para extraer texto de PDFs
def extraer_texto_documento(archivo):
    texto_extraido = ""
    if archivo.name.endswith(".pdf"):
        lector_pdf = PyPDF2.PdfReader(archivo)
        for pagina in lector_pdf.pages:
            texto_extraido += pagina.extract_text() + "\n"
    elif archivo.name.endswith(".txt"):
        texto_extraido = archivo.getvalue().decode("utf-8")
    return texto_extraido

# 5. Dibujar historial de mensajes
for mensaje in st.session_state.historial:
    with st.chat_message(mensaje["role"]):
        if "mostrar_imagen" in mensaje:
            st.image(mensaje["mostrar_imagen"], width=300)
        st.markdown(mensaje["content"])

# 6. Lógica de procesamiento
texto_usuario = st.chat_input("Escribe tu orden, o sube un archivo y pregúntame algo...")

if texto_usuario:
    modelo_actual = MODELO_TEXTO
    mensaje_usuario = {"role": "user", "content": texto_usuario}
    
    if imagen_subida:
        bytes_imagen = imagen_subida.getvalue()
        mensaje_usuario["images"] = [bytes_imagen]
        mensaje_usuario["mostrar_imagen"] = bytes_imagen
        modelo_actual = MODELO_VISION
        
    if documento_subido:
        texto_documento = extraer_texto_documento(documento_subido)
        mensaje_usuario["content"] = f"Analiza este documento:\n\n{texto_documento}\n\nOrden del usuario: {texto_usuario}"

    st.session_state.historial.append(mensaje_usuario)
    
    with st.chat_message("user"):
        if imagen_subida:
            st.image(imagen_subida, width=300)
        st.markdown(texto_usuario)
        if documento_subido:
            st.caption(f"📎 Documento adjunto: {documento_subido.name}")
            
    with st.chat_message("assistant"):
        espacio_respuesta = st.empty()
        espacio_respuesta.markdown("*Procesando...*")
        
        try:
            historial_api = []
            for msg in st.session_state.historial:
                msg_limpio = {"role": msg["role"], "content": msg["content"]}
                if "images" in msg:
                    msg_limpio["images"] = msg["images"]
                historial_api.append(msg_limpio)

            respuesta = ollama.chat(
                model=modelo_actual, 
                messages=historial_api,
                options={"num_predict": 4096, "temperature": 0.3}
            )
            
            contenido_respuesta = respuesta['message']['content']
            espacio_respuesta.markdown(contenido_respuesta)
            st.session_state.historial.append({"role": "assistant", "content": contenido_respuesta})
            
        except Exception as e:
            espacio_respuesta.error(f"Error de conexión: {e}")