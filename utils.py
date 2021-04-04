import cv2
import numpy as np


def decode_image(content):
    return cv2.imdecode(np.frombuffer(content, dtype=np.uint8), cv2.IMREAD_COLOR)
