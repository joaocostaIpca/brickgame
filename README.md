# Índice
Neste trabalho pretende-se ...


# breaker.py

Esta secção é exclusivaente reservada para as configurações e controles do Jogo em Python
 ## Definição das dimensões do ecrã e as cores do jogo:
 ```python
  SCREEN_WIDTH = 800
  SCREEN_HEIGHT = 600
  PADDLE_WIDTH = 100
  BALL_RADIUS = 10
  RED = (255, 0, 0)
  BLUE = (0, 0, 255)
  ```

## Classes

### Classe Paddle
 
**Inicializa a "paddle" na posição central inferior da janela.**
```python
def __init__(self):
    self.rect = pygame.Rect((SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - PADDLE_HEIGHT * 2),
                       (PADDLE_WIDTH, PADDLE_HEIGHT))
```  
**Move a "padddle" horizontalmente com base na posição x detectada pela webcam, limitando a posição dentro das bordas da janela.**
```python
def move(self, x):
    self.rect.x = x - PADDLE_WIDTH // 2
    if self.rect.x < 0:
        self.rect.x = 0
    if self.rect.x > SCREEN_WIDTH - PADDLE_WIDTH:
        self.rect.x = SCREEN_WIDTH - PADDLE_WIDTH
```
 **Desenha a "paddle" na tela.**
```python
def draw(self, screen):
    pygame.draw.rect(screen, BLUE, self.rect)
```
### Classe Ball
**Inicializa a bola no centro da janela com uma velocidade aleatória horizontal e uma velocidade fixa vertical.**
```python
def __init__(self):
    self.rect = pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (BALL_RADIUS * 2, BALL_RADIUS * 2))
    self.speed = [random.choice([-5, 5]), -5]
``` 
**Move a bola em ambas as direções e faz a bola "rebotar" quando atinge as paredes laterais e o topo.**
```python
def move(self):
    self.rect.x += self.speed[0]
    self.rect.y += self.speed[1]

    if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - BALL_RADIUS * 2:
        self.speed[0] = -self.speed[0]
    if self.rect.y <= 0:
        self.speed[1] = -self.speed[1]
```
**Inverte a direção vertical da bola, usado nas colisões com a paleta e tijolos.**
```python
def bounce(self):
    self.speed[1] = -self.speed[1]
```
**Desenha a bola na tela.**
 ```python
def draw(self, screen):
    pygame.draw.circle(screen, RED, (self.rect.x + BALL_RADIUS, self.rect.y + BALL_RADIUS), BALL_RADIUS)
```
### Classe Brick

**Inicializa um tijolo na posição (x, y) com uma cor aleatória.**
```python
def __init__(self, x, y):
    self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
    self.is_broken = False
    self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
```
&nbsp;
**Desenha o tijolo na tela, se ainda não tiver sido "quebrado".**
```python
def draw(self, screen):
    if not self.is_broken:
        pygame.draw.rect(screen, self.color, self.rect)
```


## Funções Auxiliares

### create_bricks()

**Cria uma lista de tijolos organizados em uma grelha, cobrindo o topo da janela.**
```python
def create_bricks():
    return [Brick(x * BRICK_WIDTH, y * BRICK_HEIGHT) for x in range(10) for y in range(5)]
```

### show_main_screen(screen)

**Exibe uma mensagem inicial na tela para o jogador começar o jogo pressionando qualquer tecla.**
```python
def show_main_screen(screen):
    screen.fill((0, 0, 0))
    text = font.render("Pressiona qualquer tecla para começar", True, WHITE)
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

## Ciclo Principal do Jogo - run_game()

### Inicialização dos Objetos

**Cria e inicializa todos os objetos do jogo, incluindo a paleta, bola e tijolos.**
```python
paddle = Paddle()
ball = Ball()
bricks = create_bricks()
lives = 2  # Vidas iniciais do jogador
```

## Ciclo do Jogo

   1. Captura vídeo e encontra a posição x de um objeto vermelho para controlar a paleta.
   2. Move a bola e verifica colisões com a paleta, tijolos e paredes.
   3. Atualiza o ecrã com as mudanças, desenhando todos os objetos.
```python
while running:
    # Captura da webcam e controlo da paleta
    ret, frame = cap.read()
    if contours:
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        paddle_x = int((x + w // 2) / frame.shape[1] * SCREEN_WIDTH)
        paddle.move(paddle_x)

    # Movimento da bola e verificações de colisões
    ball.move()
    if ball.rect.colliderect(paddle.rect):
        ball.bounce()

    for brick in bricks:
        if ball.rect.colliderect(brick.rect) and not brick.is_broken:
            brick.is_broken = True
            ball.bounce()

    # Desenha objetos no ecrã
    paddle.draw(screen)
    ball.draw(screen)
    for brick in bricks:
        brick.draw(screen)
    pygame.display.flip()
```
### Condições de Vitória e Derrota

**Verifica se o jogador "ganhou" (todos os tijolos quebrados) ou "perdeu" (perdeu todas as vidas).**
```python
if all(brick.is_broken for brick in bricks):
    # Mostrar mensagem de vitória
if ball.rect.y > SCREEN_HEIGHT:
    lives -= 1
    if lives == 0:
        # Mostrar mensagem de fim de jogo
```

# main.py






