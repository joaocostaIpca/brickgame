from ultralytics import YOLO
import cv2

class PaddleControlYOLO:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.cap = cv2.VideoCapture(0)
        # Load the YOLOv5 model
        self.model = YOLO("yolov5s.pt")  # Pre-trained YOLOv5 model

    def get_paddle_position(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture video")
            return None

        # Flip the frame horizontally for better interaction
        frame = cv2.flip(frame, 1)

        # Use YOLOv5 to detect objects in the frame
        results = self.model.predict(source=frame, conf=0.5, show=False)

        # Process the results
        detections = results[0].boxes.data  # Access the bounding boxes directly
        for detection in detections:
            x_min, y_min, x_max, y_max, confidence, class_id = detection.tolist()
            if int(class_id) == 67:  # Class ID 67 is 'cell phone' in the COCO dataset
                # Draw bounding box on the frame
                cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)

                # Calculate the center of the bounding box
                object_center_x = int((x_min + x_max) / 2)
                frame_width = frame.shape[1]
                normalized_x = object_center_x / frame_width
                paddle_x = int(normalized_x * self.screen_width)

                # Show the annotated frame
                cv2.imshow("Camera Feed with YOLO", frame)

                return paddle_x

        # If no cellphone is detected, just show the normal feed
        cv2.imshow("Camera Feed with YOLO", frame)
        return None

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
