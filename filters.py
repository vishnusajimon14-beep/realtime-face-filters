import cv2
import math


class Filters:

    @staticmethod
    def apply_glasses(frame, glasses_img, midpoint, distance, angle):

        # scale glasses based on eye distance
        width = int(distance * 2)
        height = int(width * glasses_img.shape[0] / glasses_img.shape[1])

        glasses = cv2.resize(glasses_img, (width, height))

        # ----- ROTATE GLASSES -----
        center = (width // 2, height // 2)

        rot_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        cos = abs(rot_matrix[0, 0])
        sin = abs(rot_matrix[0, 1])

        new_w = int((height * sin) + (width * cos))
        new_h = int((height * cos) + (width * sin))

        rot_matrix[0, 2] += (new_w / 2) - center[0]
        rot_matrix[1, 2] += (new_h / 2) - center[1]

        glasses = cv2.warpAffine(
            glasses,
            rot_matrix,
            (new_w, new_h),
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(0,0,0,0)
        )

        # ----- POSITION FILTER -----
        h, w = glasses.shape[:2]

        x = int(midpoint[0] - w / 2)
        y = int(midpoint[1] - h / 2)

        frame_h, frame_w = frame.shape[:2]

        # prevent going outside frame
        if x < 0 or y < 0 or x + w > frame_w or y + h > frame_h:
            return frame

        roi = frame[y:y+h, x:x+w]

        # ----- ALPHA BLENDING -----
        if glasses.shape[2] == 4:

            alpha = glasses[:,:,3] / 255.0

            for c in range(3):
                roi[:,:,c] = (1-alpha) * roi[:,:,c] + alpha * glasses[:,:,c]

        frame[y:y+h, x:x+w] = roi

        return frame
    
    @staticmethod
    def apply_crown(frame, crown_img, forehead, distance):

        width = int(distance * 2.8)
        height = int(width * crown_img.shape[0] / crown_img.shape[1])

        crown = cv2.resize(crown_img, (width, height))

        h, w = crown.shape[:2]

        x = int(forehead[0] - w / 2)
        y = int(forehead[1] - h*0.9)

        frame_h, frame_w = frame.shape[:2]

        if x < 0 or y < 0 or x + w > frame_w or y + h > frame_h:
            return frame

        roi = frame[y:y+h, x:x+w]

        if crown.shape[2] == 4:

            alpha = crown[:,:,3] / 255.0

            for c in range(3):
                roi[:,:,c] = (1-alpha) * roi[:,:,c] + alpha * crown[:,:,c]

        frame[y:y+h, x:x+w] = roi

        return frame
    
    @staticmethod
    def apply_dog_filter(frame, dog_img, forehead, nose, mouth,mouth_lower, distance):

        h_total, w_total = dog_img.shape[:2]

        # ---------------- SPLIT PNG ----------------
        ears = dog_img[0:int(h_total*0.35), :]
        nose_img = dog_img[int(h_total*0.35):int(h_total*0.55), :]
        tongue = dog_img[int(h_total*0.55):h_total, :]

        frame_h, frame_w = frame.shape[:2]

        # DOG EARS
  
        width = int(distance * 2.5)
        height = int(width * ears.shape[0] / ears.shape[1])

        ears = cv2.resize(ears, (width, height))

        h, w = ears.shape[:2]

        x = int(forehead[0] - w/2)
        y = int(forehead[1] - h)

        if 0 <= x < frame_w-w and 0 <= y < frame_h-h:

            roi = frame[y:y+h, x:x+w]

            alpha = ears[:,:,3] / 255.0

            for c in range(3):
                roi[:,:,c] = (1-alpha)*roi[:,:,c] + alpha*ears[:,:,c]

            frame[y:y+h, x:x+w] = roi


        # DOG NOSE
        width = int(distance * 2)
        height = int(width * nose_img.shape[0] / nose_img.shape[1])

        dog_nose = cv2.resize(nose_img, (width, height))

        h, w = dog_nose.shape[:2]

        x = int(nose[0] - w/2)
        y = int(nose[1] - h*0.6)

        if 0 <= x < frame_w-w and 0 <= y < frame_h-h:

            roi = frame[y:y+h, x:x+w]

            alpha = dog_nose[:,:,3] / 255.0

            for c in range(3):
                roi[:,:,c] = (1-alpha)*roi[:,:,c] + alpha*dog_nose[:,:,c]

            frame[y:y+h, x:x+w] = roi

        
        # DOG TONGUE
        mouth_open = math.hypot(
        mouth[0] - mouth_lower[0],
        mouth[1] - mouth_lower[1])

        if mouth_open>distance*0.25:
            width=int(distance*1.6)
            height = int(width * tongue.shape[0] / tongue.shape[1])

            dog_tongue = cv2.resize(tongue, (width, height))

            h, w = dog_tongue.shape[:2]
            mouth_x = (mouth[0] + mouth_lower[0]) // 2
            mouth_y = mouth_lower[1]
            x = int(mouth_x - w/2)
            y = int(mouth_y)

            if 0 <= x < frame_w-w and 0 <= y < frame_h-h:

                roi = frame[y:y+h, x:x+w]

                alpha = dog_tongue[:,:,3] / 255.0

                for c in range(3):
                    roi[:,:,c] = (1-alpha)*roi[:,:,c] + alpha*dog_tongue[:,:,c]

                frame[y:y+h, x:x+w] = roi


        return frame