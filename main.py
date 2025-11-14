import streamlit as st
import groq

# VARIABLES
altura_contenedor_chat = 600
stream_status = True

# para correr el proyecto 😎 en la terminal =  python -m streamlit run main.py 
# CONSTANTES
MODELOS = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "llama-guard-4-12b"]
AVATARES = {
    "🤠 Cowboy": "🤠",
    "🤖 Robot": "🤖",
    "🐍 Python": "🐍",
    "😎 Lentes": "😎",
    "👽 Alien": "👽"
}
# lo de arriba es para soluionar el error del avatar y eso que me arriina todo y fue mi ruina y son las 2,46 am estoy loco
# FUNCIONES

def configurar_pagina():
    st.set_page_config(page_title="El chat bot pro", page_icon="😎")
    st.title("💬 El super chad bot de brian")

    st.sidebar.title("⚙️ Configuración")

    modelo = st.sidebar.selectbox("Elegí un modelo:", options=MODELOS, index=0)
    st.sidebar.markdown("---")

    avatar_usuario = st.sidebar.selectbox("Elegí tu avatar:", options=list(AVATARES.keys()), index=0)#con esto soluciono el error del avatar
    avatar_bot = st.sidebar.selectbox("Elegí avatar del bot:", options=list(AVATARES.keys()), index=3)# y con esto tambien

    return modelo, AVATARES[avatar_usuario], AVATARES[avatar_bot]


def crear_usuario():
    st.write("Secrets disponibles:", list(st.secrets.keys()))

    clave_secreta = st.secrets["CLAVE_API"]
    return groq.Groq(api_key=clave_secreta)


def configurar_modelo(cliente, modelo_elegido, prompt_usuario):
    return cliente.chat.completions.create(
        model=modelo_elegido,
        messages=[{"role": "user", "content": prompt_usuario}],
        stream=stream_status
    )


def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})


def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.write(mensaje["content"])


def area_chat():
    contenedor = st.container(height=altura_contenedor_chat, border=True)
    with contenedor:
        mostrar_historial()


def generar_respuesta(respuesta_completa_del_bot):
    _respuesta_posta = ""
    for frase in respuesta_completa_del_bot:
        if frase.choices[0].delta.content:
            _respuesta_posta += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return _respuesta_posta


# --------------------------- IMPLEMENTACIÓN -----------------------------

def main():
    modelo_elegido, avatar_usuario, avatar_bot = configurar_pagina()
    cliente_usuario = crear_usuario()
    inicializar_estado()
    area_chat()

    prompt_del_usuario = st.chat_input("Escribí tu mensaje:")

    if prompt_del_usuario:
        actualizar_historial("user", prompt_del_usuario, avatar_usuario)
        respuesta_del_bot = configurar_modelo(cliente_usuario, modelo_elegido, prompt_del_usuario)

        if respuesta_del_bot:
            with st.chat_message("assistant", avatar=avatar_bot):
                respuesta_posta = st.write_stream(generar_respuesta(respuesta_del_bot))
                actualizar_historial("assistant", respuesta_posta, avatar_bot)
                st.rerun()


if __name__ == "__main__":
    main()

