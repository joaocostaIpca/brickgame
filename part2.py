from ultralytics import YOLO
import cv2

class PaddleControlYOLO:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.cap = cv2.VideoCapture(0)
        # Carrega o modelo YOLOv5
        self.model = YOLO("yolov5s.pt")  # Modelo YOLOv5 pre-treinado

    def get_paddle_position(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Falha ao capturar video")
            return None

        # Inverte o frame horizontalmente para melhor interacao
        frame = cv2.flip(frame, 1)

        # Usa o YOLOv5 para detectar objetos no frame
        results = self.model.predict(source=frame, conf=0.5, show=False)

        # Processa os resultados
        detections = results[0].boxes.data  # Acessa as caixas delimitadoras diretamente
        for detection in detections:
            x_min, y_min, x_max, y_max, confidence, class_id = detection.tolist()
            if int(class_id) == 67:  # ID da classe 67 é 'cell phone' no dataset COCO
                # Desenha a caixa delimitadora no frame
                cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)

                # Calcula o centro da caixa delimitadora
                object_center_x = int((x_min + x_max) / 2)
                frame_width = frame.shape[1]
                normalized_x = object_center_x / frame_width
                paddle_x = int(normalized_x * self.screen_width)

                # Exibe o frame anotado
                cv2.imshow("Camera Feed with YOLO", frame)

                return paddle_x

        # Se nenhum celular for detectado, apenas exibe o feed normal
        cv2.imshow("Camera Feed with YOLO", frame)
        return None

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
