# Índice


1. [Jogo](https://github.com/joaocostaIpca/brickgame/tree/master?tab=readme-ov-file#jogo-breakerpy)
   1.1 [Jogo](https://github.com/joaocostaIpca/brickgame/tree/master?tab=readme-ov-file#jogo-breakerpy)
3. [Fase 1](https://github.com/joaocostaIpca/brickgame/tree/master?tab=readme-ov-file#1%C2%AA-fase-algoritmos-de-segmenta%C3%A7%C3%A3o)
4. [Fase 2](https://github.com/joaocostaIpca/brickgame/tree/master?tab=readme-ov-file#2%C2%AA-fase-algoritmos-de-detec%C3%A7%C3%A3o-de-objectos)
5. [Fase 3](https://github.com/joaocostaIpca/brickgame/tree/master?tab=readme-ov-file#3%C2%AA-fase-algoritmos-de-tracking-ou-detec%C3%A7%C3%A3o-de-movimento)
6. [Extras](https://github.com/joaocostaIpca/brickgame/tree/master?tab=readme-ov-file#extras)


# Jogo (breaker.py)

### Importações e Configurações Iniciais

``` python
import pygame
import random
from main import PaddleControl
from part2 import PaddleControlYOLO

```

Importa bibliotecas necessárias:

- `pygame` é usado para os gráficos e a lógica do jogo.
- `random` Para gerar números aleatórios, para a cor dos tijolos e a velocidade da bola.
- `PaddleControl` e `PaddleControlYOLO` são classes usadas para os controles da plataforma do jogo "paddle", para além disso são usadas para integrar o jogo com visão computacional.

### Constantes do Jogo

``` python
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_RADIUS = 10
BRICK_WIDTH = 75
BRICK_HEIGHT = 30
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

```
- Isto define o tamanho da tela, do "paddle", da bola, tijolos e das cores padrão do jogo para estes elementos


## Classes Dos Objetos do Jogo

### Paddle

``` python
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - PADDLE_HEIGHT * 2),
                                (PADDLE_WIDTH, PADDLE_HEIGHT))
    def move(self, x):
        self.rect.x = x - PADDLE_WIDTH // 2
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PADDLE_WIDTH:
            self.rect.x = SCREEN_WIDTH - PADDLE_WIDTH
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)


```
Esta classe tem como função representar a "paddle"

Principais métodos:

- `__init__` Inicializa a posição da raquete.
- `move(x)` Move a raquete horizontalmente, garantindo que ela permaneça dentro da tela.
- `draw(screen)` Desenha a raquete na tela.

## Ball

``` python
class Ball:
    def __init__(self):
        self.rect = pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.speed = [random.choice([-5, 5]), -5]
    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - BALL_RADIUS * 2:
            self.speed[0] = -self.speed[0]
        if self.rect.y <= 0:
            self.speed[1] = -self.speed[1]
    def bounce(self):
        self.speed[1] = -self.speed[1]
    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.rect.x + BALL_RADIUS, self.rect.y + BALL_RADIUS), BALL_RADIUS)



```
Esta classe tem como função representar a bola do jogo 

Principais métodos:

- `__init__` Começa a posição e velocidade da bola.
- `move` Move a bola e faz com que ela colida com as bordas da janela.
- `bounce` Inverte a direção vertical da bola.
- `draw` Desenha a bola na tela.


### Brick

``` python

class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.is_broken = False
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    def draw(self, screen):
        if not self.is_broken:
            pygame.draw.rect(screen, self.color, self.rect)


```
- Isto representa os tijolos que são partidos pela bola

Principais métodos:

  - `__init__` Inicia a posição, cor e estado `is_broken` do tijolo.
  - `draw` Desenha o tijolo na tela, caso este nao tenha sido partido.

## Funções Auxiliares

### Criar Tijolos

```python

def create_bricks():
    return [Brick(x * BRICK_WIDTH, y * BRICK_HEIGHT) for x in range(10) for y in range(5)]

```
- Cria uma matriz de tijolos (10 colunas por 5 linhas), posicionados numa grade.


### Mostrar Tela Inicial

```python

def show_main_screen(screen):
    font = pygame.font.Font(None, 74)
    screen.fill((0, 0, 0))
    text = font.render("Press any key to start", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


```
- Isto mostra uma mensagem inicial ("Press any key to start") até que o jogador pressione qualquer tecla, e de seguida o jogo inicia.

## Função Principal

```python

def start_game(paddle_control):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breakout com CV")
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    running = True
    clock = pygame.time.Clock()
    lives = 2
    show_main_screen(screen)
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        paddle_x = paddle_control.get_paddle_position()
        if paddle_x is not None:
            paddle.move(paddle_x)
        ball.move()
        if ball.rect.colliderect(paddle.rect):
            ball.bounce()
        for brick in bricks:
            if ball.rect.colliderect(brick.rect) and not brick.is_broken:
                brick.is_broken = True
                ball.bounce()
        if all(brick.is_broken for brick in bricks):
            screen.fill((0, 0, 0))
            win_text = pygame.font.Font(None, 36).render("Você Venceu!", True, (0, 255, 0))
            screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False
        if ball.rect.y > SCREEN_HEIGHT:
            lives -= 1
            if lives > 0:
                ball = Ball()
            else:
                screen.fill((0, 0, 0))
                game_over_text = pygame.font.Font(None, 36).render("Fim de Jogo!", True, (255, 0, 0))
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.delay(2000)
                running = False
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)
        lives_text = pygame.font.Font(None, 36).render(f"Vidas: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 10))
        pygame.display.flip()
        clock.tick(60)
    paddle_control.release()
    pygame.quit()

```

Controla o fluxo do jogo:

- Atualiza os objetos do jogo (paddle, bola, tijolos).
- Gere as condições de vitória e derrota e mostra a mensagem do mesmo.
- Atualiza a tela em 60 FPS.

### Fluxo do Jogo
1. Mostra a tela inicial.
2. Inicia o loop principal:

   - Movimenta a bola e o paddle.
   - Detecta colisões.
   -  Exibe o estado atual das vidas e dos "bricks" partidos.

3. Termina o jogo em caso de vitória ou derrota.


# 1ª Fase Algoritmos de Segmentação

### Bibliotecas Importadas
``` python
import cv2
import numpy as np

```
- `cv2` Biblioteca OpenCV, processa as imagens e a webcam.
- `numpy (np)` Biblioteca para manipulação de arrays, usada aqui para criar máscaras de cores.

## Classe PaddleControl

Essa classe serve para capturar o movimento de um objeto vermelho na câmera e traduzir sua posição horizontal para a tela do jogo.

### Construtor (__init__)

``` python


class PaddleControl:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.cap = cv2.VideoCapture(0)
        self.lower_red1 = np.array([0, 120, 70], dtype=np.uint8)
        self.upper_red1 = np.array([10, 255, 255], dtype=np.uint8)
        self.lower_red2 = np.array([170, 120, 70], dtype=np.uint8)
        self.upper_red2 = np.array([180, 255, 255], dtype=np.uint8)


```
- `screen_width` Largura da tela do jogo, é utilizada para mapear a posição detectada no vídeo para o espaço do jogo.
- `cv2.VideoCapture(0)` Inicia a captura de vídeo da câmera.

### Limites de cor vermelha 

- Vermelho no espaço HSV é dividido em duas faixas (tons próximos de 0 e 180 graus no círculo HSV):
    - Faixa 1: ![0, 120, 70](https://placehold.co/15x15/b38f8f/b38f8f.png) `[0, 120, 70]` a ![10, 255, 255](https://placehold.co/15x15/ff2a00/ff2a00.png) `[10, 255, 255]`.
    - Faixa 2: ![170, 120, 70](https://placehold.co/15x15/8fb3ad/8fb3ad.png) `[170, 120, 70]` a ![180, 255, 255](https://placehold.co/15x15/00ffff/00ffff.png) `[180, 255, 255]`.

>Nota:
>O código utiliza faixas de valores no espaço de cor HSV, onde a faixa [170, 180] de Hue corresponde ao extremo do vermelho `não ao azul` apesar de parecer visualmente semelhante a um tom de azul. `O espaço HSV é circular` e o vermelho estende-se de 0 a 10 e de 170 a 180, criando essa sobreposição. A detecção no código é limitada a objetos vermelhos, e a saturação e valor ajustados restringem ainda mais a detecção. O mesmo poderá ser observado no seguinte esquema que exemplifica os valores de vermelho um espaço HSV.
>![esquemaHSV](https://i.sstatic.net/gyuw4.png)

Hue (Tonalidade):
- 0 a 360° em graus ou 0 a 179 em OpenCV.
    - Vermelho aparece em duas regiões:
      - Início: 0–10 (vermelho claro).
      - Fim: 170–180 (vermelho profundo).

Saturation (Saturação):
- (120–255), assim descarta as cores mais pálidas.

Value (Brilho):
- Deteta objetos com brilho moderado a alto (70–255).

## Função get_paddle_position

Esta Função possui o objetivo de identificar a posição horizontal de um objeto vermelho na camara e traduzir para o jogo o seu movimento


### Captura de video 
``` python


ret, frame = self.cap.read()
if not ret:
    print("Falha ao capturar video")
    return None


```
- Isto Captura o video e se caso nao consiga imprime erro

### Pré Processamento da Imagem
``` python


frame = cv2.flip(frame, 1)
hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


```
- `cv2.flip(frame, 1)` Inverte horizontalmente o frame pois a camara detecta ao contrario, assim se eu mover para a direita na vida real o programa não deteta que foi para esquerda.
- `cv2.cvtColor` Converte o frame de BGR (formato padrão do OpenCV) para HSV,assim torna mais fácil a detecção de cores.

### Máscara Cor Vermelha
``` python

mask1 = cv2.inRange(hsv_frame, self.lower_red1, self.upper_red1)
mask2 = cv2.inRange(hsv_frame, self.lower_red2, self.upper_red2)
red_mask = cv2.bitwise_or(mask1, mask2)



```

- `cv2.inRange` Cria uma máscara binária, onde pixels dentro dos limites especificados são 1 (branco), e fora são 0 (preto). 

Combinação das faixas: 

  - `mask1` Deteta a primeira tela de vermelho.
  - `mask2` Deteta a segunda tela de vermelho.
  - `red_mask` Combina as duas máscaras com o uso do `cv2.bitwise_or`

### Operações Morfológicas

``` python
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
red_mask = cv2.erode(red_mask, kernel, iterations=2)
red_mask = cv2.dilate(red_mask, kernel, iterations=2)
red_mask = cv2.GaussianBlur(red_mask, (3, 3), 0)



```

Operações para melhorar a qualidade da máscara:
- `Erosão` Remove pequenos ruídos ao reduzir algumasregiões brancas.
- `Dilatação` Reforça as regiões brancas restantes.
- `Desfoque Gaussiano` Suaviza as bordas da máscara.

> Nota:
> Apesar de não ser extramente necessário etas operações apenas são usadas para melhorar a experienciam a Erosão e a Dilatação podem ser encontradas no seguinte link https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html e o Ddesfoque Gaussiano pode ser encontrado no seguinte https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html

### Detetar Contornos

``` python
contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if contours:
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    object_center_x = x + w // 2
    frame_width = frame.shape[1]
    normalized_x = object_center_x / frame_width
    paddle_x = int(normalized_x * self.screen_width)




```

- `cv2.findContours` Encontra contornos na máscara binária.

- `Maior contorno` Seleciona o contorno com a maior área de cor vermelha detetada.

- `cv2.boundingRect` Calcula a menor caixa retangular que envolve o contorno, através das coordenadas e dimensoes da caixa(x, y, w, h).
 
 
Cálculo da posição horizontal `paddle_x`: 
    - Determina o centro horizontal do objeto `object_center_x`.
    - Normaliza a posição em relação à largura do tamnaho da tela.
    - Converte a posição para a largura da tela do jogo.

### Mostrar o Feedback Visual

``` python
cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.imshow("Camera Feed", frame)
cv2.imshow("Contour Feed", red_mask)


```

- Desenha um retângulo por volta do objeto vermelho detetado.
 
Mostra dois feeds:
  - `Camera Feed` Feed da câmera com o retângulo desenhado.
  - `Contour Feed` Máscara binária, que mostra o objeto que foi detetado.

## Resumo da primeira fase

1. Captura um frame da câmera e o converte para HSV.
2. Cria uma máscara binária para detectar objetos vermelhos.
3. Melhora a qualidade da máscara binária.
4. Encontra o maior contorno na máscara e calcula sua posição horizontal.
5. Devolvve a posição que foi obtida para a tela do jogo.
6. Mostra a camrara com o retangulo ao redor de objetos vermelhos e a máscara binária .


# 2ª Fase Algoritmos de Detecção de Objectos



# 3ª Fase Algoritmos de Tracking ou Detecção de Movimento




# Extras



# WebGrafia

https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
https://cvexplained.wordpress.com/2020/04/28/color-detection-hsv/ 



