import cv2
import numpy as np
from breaker import SCREEN_WIDTH

# Configuração do OpenCV
cap = cv2.VideoCapture(0)
lower_red1 = np.array([0, 120, 70], dtype=np.uint8)
upper_red1 = np.array([10, 255, 255], dtype=np.uint8)
lower_red2 = np.array([170, 120, 70], dtype=np.uint8)
upper_red2 = np.array([180, 255, 255], dtype=np.uint8)

# Loop de captura de vídeo
while True:
    # Capturar frame da webcam
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar vídeo")
        break

    frame = cv2.flip(frame, 1)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Criar máscara para o objeto vermelho
    mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Operações morfológicas para refinar a máscara
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    red_mask = cv2.erode(red_mask, kernel, iterations=2)
    red_mask = cv2.dilate(red_mask, kernel, iterations=2)
    red_mask = cv2.GaussianBlur(red_mask, (3, 3), 0)

    # Encontrar contornos na máscara
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Encontrar o maior contorno e calcular a posição do objeto
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        object_center_x = x + w // 2
        frame_width = frame.shape[1]
        normalized_x = object_center_x / frame_width
        paddle_x = int(normalized_x * SCREEN_WIDTH)

        # Exibir retângulo em torno do objeto detectado
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Mostrar o feed da câmera e a máscara
    cv2.imshow("Camera Feed", frame)
    cv2.imshow("Máscara do Objeto Vermelho", red_mask)

    # Encerrar ao pressionar a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
