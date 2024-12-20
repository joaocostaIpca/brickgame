import cv2
import numpy as np

class PaddleControlMeanShift:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.cap = cv2.VideoCapture(0)

        # Variáveis para rastreamento
        self.track_window = None
        self.roi_hist = None

        # Inicializa o rastreamento
        self.initialize_tracker()

    def initialize_tracker(self):
        """Permite ao usuário selecionar manualmente a área contendo a cor vermelha para rastrear com MeanShift."""
        ret, frame = self.cap.read()
        if not ret:
            print("Falha ao capturar o vídeo durante a inicialização")
            return

        # Inverte o frame horizontalmente
        frame = cv2.flip(frame, 1)

        # Permitir ao usuário selecionar a região que contém o objeto vermelho
        roi = cv2.selectROI("Selecione a região do objeto vermelho", frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Selecione a região do objeto vermelho")

        if roi != (0, 0, 0, 0):  # Verifica se uma área foi selecionada
            # Captura a região selecionada
            x, y, w, h = roi
            self.track_window = (x, y, w, h)
            roi_frame = frame[y:y + h, x:x + w]

            # Converte a ROI para o espaço de cor HSV
            hsv_roi = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)

            # Aqui selecionamos apenas a cor vermelha na região, sem média
            lower_red1 = np.array([0, 120, 70])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 120, 70])
            upper_red2 = np.array([180, 255, 255])

            # Criar máscaras para isolar a cor vermelha
            mask1 = cv2.inRange(hsv_roi, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv_roi, lower_red2, upper_red2)
            mask = cv2.bitwise_or(mask1, mask2)

            # Aplica a máscara para extrair a cor vermelha
            red_region = cv2.bitwise_and(roi_frame, roi_frame, mask=mask)

            # Calcula o histograma da cor vermelha na ROI
            self.roi_hist = cv2.calcHist([cv2.cvtColor(red_region, cv2.COLOR_BGR2HSV)], [0, 1], None, [180, 256], [0, 180, 0, 256])
            cv2.normalize(self.roi_hist, self.roi_hist, 0, 255, cv2.NORM_MINMAX)

        else:
            print("Nenhuma área foi selecionada.")
            return

    def get_paddle_position(self):
        """Usa o MeanShift para rastrear a cor vermelha e retornar a posição normalizada da paddle."""
        ret, frame = self.cap.read()
        if not ret:
            print("Falha ao capturar vídeo")
            return None

        # Inverte o frame horizontalmente
        frame = cv2.flip(frame, 1)

        # Converte o frame para o espaço de cor HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Calcula a backprojection (projeção reversa) usando o histograma da cor vermelha
        back_proj = cv2.calcBackProject([hsv_frame], [0, 1], self.roi_hist, [0, 180, 0, 256], 1)

        # Aplica o algoritmo MeanShift
        ret, self.track_window = cv2.meanShift(back_proj, self.track_window,
                                               (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 50, 1))

        # Desenha o retângulo ao redor da área rastreada
        x, y, w, h = self.track_window
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calcula a posição da paddle com base no centro da região rastreada
        frame_width = frame.shape[1]
        normalized_x = (x + w / 2) / frame_width
        paddle_x = int(normalized_x * self.screen_width)

        # Exibe a posição da paddle
        cv2.imshow("Camera Feed with Red Detection and MeanShift Tracking", frame)
        return paddle_x

    def release(self):
        """Libera recursos."""
        self.cap.release()
        cv2.destroyAllWindows()
