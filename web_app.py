import streamlit as st
from datetime import datetime
import pickle
import fractions
import matplotlib.pyplot as plt
from utils import data_utils as dt
from betsi.image import betsi
from streamlit_webrtc import WebRtcMode, create_video_source_track, webrtc_streamer


# C:\Users\hugo.gavilima\OneDrive - Universidad de Las Américas\Documentos\TAREAS\BETSI\
# streamlit run web_app.py --theme.base dark
 
#----------------------------------------------------------------------------------------
#Definimos la apliacion
utils_ = dt.paths_().get_json("utils\web.json")
# Título de la página
st.write("# BETSI")
st.write("### Conteo de Objetos en Entornos Complejos de Alta Densidad")

# Sidebar con lista desplegable
option = st.sidebar.selectbox(
    'Seleccione una opción:',
    utils_["lts"]
)

valor = st.sidebar.slider(
    "Selecciona un valor", 
    min_value=0.0, max_value=1.0, value=0.5, step=0.01
)

texto = None
if option == utils_["lts"][1]:
    texto = st.sidebar.text_input("Ingrese la dirección IP de la cámara.", "http://10.111.20.134:8080/video")
#----------------------------------------------------------------------------------------


#Definimos los paramaetros del video a presentar
fps = 35

cache_key = "betsi"
if cache_key in st.session_state:
    betsi_ = st.session_state[cache_key]
else:
    betsi_ = betsi(name_ip=texto, score_threshold = valor)
    st.session_state[cache_key] = betsi_
    

#betsi_ = betsi(name_ip=texto, score_threshold = valor)
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

boton = st.button("Tomar Registro")
if boton:
    frame, detections = betsi_.get_all(pts = 0, time_base = fractions.Fraction())
    res = {"frame": frame, "detections": detections}
    name = f"image_capture/Captura {datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.pkl"
    dt.paths_().set_pickle(name, res)
    
    
    
    

    
    


    



