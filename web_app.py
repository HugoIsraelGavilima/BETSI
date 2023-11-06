import streamlit as st
from utils import data_utils as dt
from betsi.image import betsi
from streamlit_webrtc import WebRtcMode, create_video_source_track, webrtc_streamer


# C:\Users\hugo.gavilima\OneDrive - Universidad de Las Américas\Documentos\TAREAS\BETSI\
# streamlit run web_app.py --theme.base dark
 
#----------------------------------------------------------------------------------------
#Definimos la apliacion
utils_ = dt.paths_().get_json("utils/web.json")
# Título de la página
st.write("# BETSI")
st.write("### Conteo de Objetos en Entornos Complejos de Alta Densidad")

# Sidebar con lista desplegable
option = st.sidebar.selectbox(
    'Seleccione una opción:',
    utils_["lts"]
)

texto = None
if option == utils_["lts"][1]:
    texto = st.sidebar.text_input("Ingrese la dirección IP de la cámara.")
#----------------------------------------------------------------------------------------


#Definimos los paramaetros del video a presentar
fps = 10

cache_key = "betsi"
if cache_key in st.session_state:
    betsi_ = st.session_state[cache_key]
else:
    betsi_ = betsi()
    st.session_state[cache_key] = betsi_


webrtc_ctx = webrtc_streamer(
    key="object-detection",
    mode=WebRtcMode.SENDRECV,
     rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    video_frame_callback=betsi_.video_frame_callback,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)
