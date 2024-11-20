import cv2
import numpy as np

class PaddleControl:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.cap = cv2.VideoCapture(0)  # Inicializa a captura de video
        self.lower_red1 = np.array([0, 120, 70], dtype=np.uint8)  # Limites inferiores para a cor vermelha
        self.upper_red1 = np.array([10, 255, 255], dtype=np.uint8)  # Limites superiores para a cor vermelha
        self.lower_red2 = np.array([170, 120, 70], dtype=np.uint8)  # Limites inferiores para a cor vermelha (segunda faixa)
        self.upper_red2 = np.array([180, 255, 255], dtype=np.uint8)  # Limites superiores para a cor vermelha (segunda faixa)

    def get_paddle_position(self):
        ret, frame = self.cap.read()  # Captura um frame da camera
        if not ret:
            print("Falha ao capturar video")
            return None

        # Inverter o frame e converter para o espaco de cores HSV
        frame = cv2.flip(frame, 1)  # Inverte horizontalmente
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Converte para HSV

        # Mascara para detectar objetos vermelhos
        mask1 = cv2.inRange(hsv_frame, self.lower_red1, self.upper_red1)  # Primeira faixa de vermelhos
        mask2 = cv2.inRange(hsv_frame, self.lower_red2, self.upper_red2)  # Segunda faixa de vermelhos
        red_mask = cv2.bitwise_or(mask1, mask2)  # Combina as duas mascaras

        # Operacoes morfologicas para melhorar a mascara
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))  # Cria um elemento estrutural em forma de elipse
        red_mask = cv2.erode(red_mask, kernel, iterations=2)  # Erosao para remover pequenos ruidos
        red_mask = cv2.dilate(red_mask, kernel, iterations=2)  # Dilatacao para reforcar as regioes detectadas
        red_mask = cv2.GaussianBlur(red_mask, (3, 3), 0)  # Aplica um desfoque gaussiano para suavizar a mascara

        # Encontrar contornos na mascara
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)  # Pega o maior contorno
            x, y, w, h = cv2.boundingRect(largest_contour)  # Obtem a caixa delimitadora do maior contorno
            object_center_x = x + w // 2  # Calcula o centro do objeto no eixo X
            frame_width = frame.shape[1]  # Largura do frame
            normalized_x = object_center_x / frame_width  # Normaliza a posicao do centro do objeto
            paddle_x = int(normalized_x * self.screen_width)  # Calcula a posicao do paddle na tela

            # Desenha o retangulo no feed da camera normal
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Exibe o feed da camera normal com o retangulo desenhado
            cv2.imshow("Camera Feed", frame)

            # Exibe a mascara para os contornos
            cv2.imshow("Contour Feed", red_mask)

            return paddle_x  # Retorna a posicao do paddle

        # Se nenhum objeto for detectado, mostra os feeds sem atualizacoes
        cv2.imshow("Camera Feed", frame)
        cv2.imshow("Contour Feed", red_mask)
        return None

    def release(self):
        self.cap.release()  # Libera a camera
        cv2.destroyAllWindows()  # Fecha todas as janelas do OpenCV
