class LandmarkExtractor:
    @staticmethod
    def extract(face):
        points={
            "left_eye": face[33],
            "right_eye": face[263],
            "nose": face[4],
            "mouth": face[13],
            "mouth_lower":face[14],
            "chin": face[152],
            "forehead": face[10]
        }
        return points