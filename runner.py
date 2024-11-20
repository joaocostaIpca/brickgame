import pygame
from breaker import start_game,SCREEN_WIDTH
from main import PaddleControl
from part2 import PaddleControlYOLO

def main(use_yolo=False):
    # Escolhe qual metodo de controlo, o que esta pre defenido e o com yolo
    if use_yolo:
        paddle_control = PaddleControlYOLO(SCREEN_WIDTH)
    else:
        paddle_control = PaddleControl(SCREEN_WIDTH)

    # Começa o jogo
    start_game(paddle_control)

if __name__ == "__main__":
    main(use_yolo=True)  # Mude para True para usar YOLO e false para hsv
