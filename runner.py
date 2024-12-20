import pygame
from breaker import start_game,SCREEN_WIDTH
from part1 import PaddleControl
from part2 import PaddleControlYOLO

def start_hsv():
    print("Método escolhido: HSV")
    paddle_control = PaddleControl(SCREEN_WIDTH)
    start_game(paddle_control)

def start_yolo():
    print("Método escolhido: YOLO")
    paddle_control = PaddleControlYOLO(SCREEN_WIDTH)
    start_game(paddle_control)

def start_bytetrack():
    print("Método escolhido: ByteTrack")
    paddle_control = PaddleControlByteTrack(SCREEN_WIDTH)
    start_game(paddle_control)

# Função principal para menu no terminal
def main_menu():
    while True:
        print("1. Parte 1 (HSV)")
        print("2. Parte 2 (YOLO)")
        print("3. Parte 3 (ByteTrack)")
        print("0. Sair")

        choice = input("Qual: ")

        if choice == "1":
            start_hsv()
            break
        elif choice == "2":
            start_yolo()
            break
        elif choice == "3":
            start_bytetrack()
            break
        elif choice == "0":
            break
        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    main_menu()
