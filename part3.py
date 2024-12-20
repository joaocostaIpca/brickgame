from ultralytics import YOLO
import cv2
from bytetrack import BYTETracker, STrack


class PaddleControlByteTrack:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.cap = cv2.VideoCapture(0)

        # Carrega o modelo YOLO para detecção de objetos
        self.model = YOLO("yolov5s.pt")  # Modelo YOLOv5 pre-treinado

        # Inicializa o ByteTrack
        self.tracker = BYTETracker(frame_rate=30)  # Configuração do ByteTrack com taxa de quadros padrão

    def get_paddle_position(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Falha ao capturar video")
            return None

        # Inverte o frame horizontalmente para melhor interação
        frame = cv2.flip(frame, 1)

        # Usa o YOLOv5 para detectar objetos no frame
        results = self.model.predict(source=frame, conf=0.5, show=False)

        # Processa os resultados de detecção
        detections = []
        for detection in results[0].boxes.data:
            x_min, y_min, x_max, y_max, confidence, class_id = detection.tolist()
            if int(class_id) == 67:  # Classe 67 é 'cell phone' no dataset COCO
                detections.append([x_min, y_min, x_max, y_max, confidence])

        # Converte as detecções para o formato esperado pelo ByteTrack
        detections = [STrack([x_min, y_min, x_max, y_max, conf], 67) for x_min, y_min, x_max, y_max, conf in detections]

        # Atualiza o ByteTrack com as detecções atuais
        tracks = self.tracker.update(detections)

        for track in tracks:
            if track.state == STrack.State.Tracked:  # Garante que o objeto está sendo rastreado
                x_min, y_min, x_max, y_max = track.tlwh

                # Calcula o centro do objeto rastreado
                object_center_x = int((x_min + x_max) / 2)
                frame_width = frame.shape[1]
                normalized_x = object_center_x / frame_width
                paddle_x = int(normalized_x * self.screen_width)

                # Desenha a caixa delimitadora no frame
                cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)

                # Exibe o frame anotado
                cv2.imshow("Camera Feed with ByteTrack", frame)

                return paddle_x

        # Se nenhum objeto for rastreado, apenas exibe o feed normal
        cv2.imshow("Camera Feed with ByteTrack", frame)
        return None

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()