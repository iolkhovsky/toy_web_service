import base64
import cv2
import io
import numpy as np
from pydantic import BaseModel


class ProcessingItem(BaseModel):
    file: str
    EncodedImg: str


def decode_image(content):
    return cv2.imdecode(np.frombuffer(content, dtype=np.uint8), cv2.IMREAD_COLOR)
