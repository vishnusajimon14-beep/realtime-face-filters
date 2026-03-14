import cv2
from face_mesh import FaceMeshDetector
from landmark import LandmarkExtractor
from geometry import FaceGeometry
from filters import Filters


def main():

    cap = cv2.VideoCapture(0)
    detector = FaceMeshDetector()

    glasses_img = cv2.imread(r"C:\Users\vishn\data science\project\snapchat filter\assests\12-2-glasses-png-pic.png", cv2.IMREAD_UNCHANGED)
    crown_img=cv2.imread(r"C:\Users\vishn\data science\project\snapchat filter\assests\crown.png",cv2.IMREAD_UNCHANGED)
    dog_img=cv2.imread(r"C:\Users\vishn\data science\project\snapchat filter\assests\dog.png",cv2.IMREAD_UNCHANGED)
    filter_mode = 0   # 0 = mesh , 1 = glasses ,2=CROWN

    while True:

        ret, frame = cap.read()

        if not ret:
            print("no access to webcam")
            break

        frame = cv2.flip(frame, 1)

        faces = detector.detect(frame)

        for face in faces:

            points = LandmarkExtractor.extract(face)

            left_eye = points["left_eye"]
            right_eye = points["right_eye"]
            nose = points["nose"]
            forehead=points["forehead"]
            mouth=points["mouth"]
            mouth_lower=points["mouth_lower"]

            distance = FaceGeometry.eye_distance(left_eye, right_eye)
            midpoint = FaceGeometry.eye_midpoint(left_eye, right_eye)
            angle = FaceGeometry.head_angle(left_eye, right_eye)

            if filter_mode == 0:
                frame = detector.draw_mesh(frame, faces)

            elif filter_mode == 1:
                frame = Filters.apply_glasses(frame, glasses_img, midpoint, distance,angle)
            
            elif filter_mode == 2:
                frame = Filters.apply_crown(frame, crown_img, forehead, distance)

            elif filter_mode == 3:
                frame = Filters.apply_dog_filter(frame,dog_img,forehead,nose,mouth,mouth_lower,distance)

            cv2.putText(frame, f"Dist: {int(distance)}", (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

            cv2.putText(frame, f"Angle: {int(angle)}", (20,70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

        cv2.imshow("webcam", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        if key == ord('0'):
            filter_mode = 0

        if key == ord('1'):
            filter_mode = 1

        if key == ord('2'):
            filter_mode = 2
        if key==ord('3'):
            filter_mode=3
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()