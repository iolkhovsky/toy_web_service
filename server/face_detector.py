import cv2
import numpy as np
import sys


class FaceDetector:

    def __init__(self):
        self._clf = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def __call__(self, img):
        assert isinstance(img, np.ndarray), f"Wrong type of input image: {type(img)}"
        assert len(img.shape) == 3 and img.shape[2] == 3
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self._clf.detectMultiScale(gray, 1.1, 4)
        visualization = img.copy()
        for x, y, w, h in faces:
            cv2.rectangle(visualization, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return visualization, faces

if __name__ == "__main__":
    detector = FaceDetector()
    if len(sys.argv) > 1:
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
    else:
        img = cv2.imread("faces.jpeg")
        processed_img, faces = detector(img)
        print("Detections:")
        for detection in faces:
            print(detection)
        cv2.imwrite("processed.jpg", processed_img)
