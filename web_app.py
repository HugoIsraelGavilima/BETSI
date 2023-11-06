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
    betsi_ = betsi(name_ip=None)
    st.session_state[cache_key] = betsi_


# video_source_track = create_video_source_track(
#     betsi(name_ip=None).get_image, key="video_source_track", fps=fps
# )

video_source_track = create_video_source_track(
    betsi_.get_image, key="video_source_track", fps=fps
)


def on_change():
    ctx = st.session_state["player"]
    stopped = not ctx.state.playing and not ctx.state.signalling
    
    # if paused: 
    #     st.text("Se pausó el video")
    if stopped:
        video_source_track.stop()  # Manually stop the track.


 
webrtc_streamer(
    key="player",
    mode=WebRtcMode.RECVONLY,
    source_video_track=video_source_track,
    media_stream_constraints={"video": True, "audio": False},
    on_change=on_change,
)


    
    


    



