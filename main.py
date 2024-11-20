import cv2
import numpy as np

class PaddleControl:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.cap = cv2.VideoCapture(0)
        self.lower_red1 = np.array([0, 120, 70], dtype=np.uint8)
        self.upper_red1 = np.array([10, 255, 255], dtype=np.uint8)
        self.lower_red2 = np.array([170, 120, 70], dtype=np.uint8)
        self.upper_red2 = np.array([180, 255, 255], dtype=np.uint8)

    def get_paddle_position(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture video")
            return None

        # Flip and convert to HSV
        frame = cv2.flip(frame, 1)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Mask for red objects
        mask1 = cv2.inRange(hsv_frame, self.lower_red1, self.upper_red1)
        mask2 = cv2.inRange(hsv_frame, self.lower_red2, self.upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)

        # Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        red_mask = cv2.erode(red_mask, kernel, iterations=2)
        red_mask = cv2.dilate(red_mask, kernel, iterations=2)
        red_mask = cv2.GaussianBlur(red_mask, (3, 3), 0)

        # Find contours
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            object_center_x = x + w // 2
            frame_width = frame.shape[1]
            normalized_x = object_center_x / frame_width
            paddle_x = int(normalized_x * self.screen_width)

            # Draw rectangle on the normal camera feed
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Show the normal camera feed with rectangle
            cv2.imshow("Camera Feed", frame)

            # Show the mask for contours
            cv2.imshow("Contour Feed", red_mask)

            return paddle_x

        # If no object detected, show feeds without updates
        cv2.imshow("Camera Feed", frame)
        cv2.imshow("Contour Feed", red_mask)
        return None

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
