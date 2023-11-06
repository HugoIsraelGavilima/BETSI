import numpy as np
import fractions
import cv2
import av
from typing import List, NamedTuple
import utils.data_utils as dt
from streamlit_webrtc import VideoTransformerBase


class betsi(VideoTransformerBase):
    def __init__(self) -> None:
        self.thickness = 2
        self.score_threshold = 0.5
        self.classes = dt.paths_().get_json("utils/config_plot.json")["clases"]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        
        self.model = cv2.dnn.readNetFromCaffe(
            "./betsi/model/betsi.prototxt.txt",
            "./betsi/model/betsi.caffemodel"
            )
    def make_predicition(self, image):
        blob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)), 
            0.007843, (300, 300), 127.5
        )
        #Hacemos la prediccion
        self.model.setInput(blob)
        output = self.model.forward().squeeze()
        
        return output[output[:, 2] >= self.score_threshold]        
    
    def video_frame_callback(self, frame: av.VideoFrame)-> av.VideoFrame:
        
        altura, ancho = frame.shape[:2]
        output = self.make_predicition(frame)
        detections = [
                Detection(
                    class_id=int(detection[1]),
                    label=self.classes[int(detection[1])],
                    score=float(detection[2]),
                    box=(detection[3:7] * np.array([ancho, altura, ancho, altura])),
                )
                for detection in output
            ]
        count_people = len([detection.label in ["person"] for detection in detections])
        frame = cv2.putText(
                frame,
                text = f"Registro: {int(count_people)} personas",
                org = (0, 32),
                fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                fontScale = 1.0,
                color = (255, 255, 0),
                thickness = self.thickness,
                lineType = cv2.LINE_4,
            )
        
        
        for detection in detections:
            caption = f"{detection.label}: {round(detection.score * 100, 2)}%"
            color = self.colors[detection.class_id]
            xmin, ymin, xmax, ymax = detection.box.astype("int")

            frame = cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
            frame = cv2.putText(
                    frame,
                    caption,
                    (xmin, ymin - 15 if ymin - 15 > 15 else ymin + 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2,
                )
        
                
        return frame


#--------------------------------------------------------------------
class Detection(NamedTuple):
    class_id: int
    label: str
    score: float
    box: np.ndarray