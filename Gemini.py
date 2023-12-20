import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
from dotenv import load_dotenv
from PIL import Image
import os
import io

# Carga variables de entorno
load_dotenv()

# Conversión de imagen a bytes
def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

# Configuración de la API de Google
API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

# Configuración de la barra lateral
def setup_sidebar():
    st.sidebar.image("bcu.png", width=180)
    st.sidebar.title('Gemini AI Explorer')
    st.sidebar.markdown('''
    **Instrucciones de uso**
    
    - Utiliza Gemini Pro para interactuar con modelos de lenguaje avanzados mediante texto.
    - Explora Gemini Pro Vision cargando imágenes y proporcionando un texto de entrada para obtener resultados visuales enriquecidos.
    - Navega entre las pestañas de Gemini Pro y Gemini Pro Vision para experimentar con diferentes tipos de entradas y modelos.
    ''')

    st.sidebar.markdown('''
    **Acerca de la aplicación**
    
    - Gemini AI Explorer te permite explorar las capacidades de los modelos de inteligencia artificial de Gemini Pro y Gemini Pro Vision.
    - Desarrollada utilizando Streamlit, esta aplicación facilita la interacción con modelos de IA de última generación.
    ''')
    st.sidebar.write('Desarrollado por [Diego Fernández](https://www.linkedin.com/in/diego-fernandez-728a35206/)')

    st.sidebar.markdown('''
    **Grupo de Desarrollo**
    
    Esta aplicación ha sido desarrollada en el grupo **ARISE: Artificial Intelligence Research in Statistics and Economics** del Banco Central del Uruguay.
    ''')

def main():
    setup_sidebar()

    st.image("./Google-Gemini-AI-Logo.png", width=200)

    gemini_pro, gemini_vision = st.tabs(["Gemini Pro", "Gemini Pro Vision"])

    with gemini_pro:
        st.header("Interactua con Gemini Pro")

        prompt = st.text_input("Ingresa prompt por favor...", placeholder="Prompt")
        model = genai.GenerativeModel("gemini-pro")

        if st.button("SEND", use_container_width=True):
            response = model.generate_content(prompt)
            st.markdown(response.text)

    with gemini_vision:
        st.header("Interactua con Gemini Pro Vision")

        image_prompt = st.text_input("Interactua con la imagen", placeholder="Prompt")
        uploaded_file = st.file_uploader("Escoge una imagen", accept_multiple_files=False, type=["png", "jpg", "jpeg", "img", "webp"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)

        if st.button("GET RESPONSE", use_container_width=True):
            model = genai.GenerativeModel("gemini-pro-vision")

            if uploaded_file is not None:
                if image_prompt != "":
                    response = model.generate_content(
                        glm.Content(
                            parts=[
                                glm.Part(text=image_prompt),
                                glm.Part(
                                    inline_data=glm.Blob(
                                        mime_type="image/jpeg",
                                        data=image_to_byte_array(image)
                                    )
                                )
                            ]
                        )
                    )
                    response.resolve()
                    st.markdown(response.text)
                else:
                    st.error("Por favor carga una imagen")
            else:
                st.error("Por favor carga una imagen")

if __name__ == "__main__":
    main()

