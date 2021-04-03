import cv2
import numpy as np
from os.path import isfile


class FaceDetector:

    def __init__(self):
        config_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        assert isfile(config_path)
        self._clf = cv2.CascadeClassifier(config_path)

    def __call__(self, img):
        assert isinstance(img, np.ndarray), f"Wrong type of input image: {type(img)}"
        assert len(img.shape) == 3 and img.shape[2] == 3
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detections = self._clf.detectMultiScale(gray, 1.1, 4)
        visualization = img.copy()
        for x, y, w, h in detections:
            cv2.rectangle(visualization, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return visualization, detections


if __name__ == "__main__":
    detector = FaceDetector()
    cam_id = 0
    cam = cv2.VideoCapture(cam_id)
    while True:
        ret, img = cam.read()
        if not ret:
            print(f"Can't capture image from the device {cam_id}")
            break
        processed_img, faces = detector(img)
        cv2.imshow("Stream", processed_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
