import base64
import cv2
import io
import numpy as np
from pydantic import BaseModel


class ProcessingItem(BaseModel):
    RequestId: str
    EncodedImg: str


def base64str_to_img(base64str):
    base64_img_bytes = base64str.encode('utf-8')
    base64bytes = base64.b64decode(base64_img_bytes)
    bytes_io = io.BytesIO(base64bytes)
    encoded = np.frombuffer(buffer=bytes_io.read(), dtype=np.uint8)
    return cv2.imdecode(encoded, cv2.IMREAD_COLOR)
