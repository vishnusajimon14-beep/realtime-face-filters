import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FaceMeshDetector:

    def __init__(self, model_path="face_landmarker.task"):

        base_options = python.BaseOptions(model_asset_path=model_path)

        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            num_faces=2
        )

        self.detector = vision.FaceLandmarker.create_from_options(options)


    def detect(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = self.detector.detect(mp_image)

        faces = []

        h, w, _ = frame.shape

        if result.face_landmarks:

            for face_landmarks in result.face_landmarks:

                points = []

                for lm in face_landmarks:

                    x = int(lm.x * w)
                    y = int(lm.y * h)

                    points.append((x, y))

                faces.append(points)

        return faces


    def draw_mesh(self, frame, faces):

        for face in faces:
            for (x, y) in face:
                cv2.circle(frame, (x, y), 1, (0,255,0), -1)

        return frame