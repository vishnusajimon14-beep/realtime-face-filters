import math
class FaceGeometry:
    @staticmethod
    def eye_distance(left_eye,right_eye):
        dx=(right_eye[0]-left_eye[0])
        dy=(right_eye[1]-left_eye[1])

        return math.hypot(dx,dy)
    
    @staticmethod
    def eye_midpoint(left_eye,right_eye):
        x=(left_eye[0]+right_eye[0])//2
        y=(left_eye[1]+right_eye[1])//2

        return (x,y)
    
    @staticmethod
    def head_angle(left_eye,right_eye):
        dx=right_eye[0]-left_eye[0]
        dy=right_eye[1]-left_eye[1]

        angle=math.degrees(math.atan2(dy,dx))

        return angle