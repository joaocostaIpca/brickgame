import pygame
import random
from main import PaddleControl  # ou de part2 import PaddleControlYOLO
from part2 import PaddleControlYOLO  # Garanta que isto está incluído se usar YOLO

# Constantes do jogo
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

# Objetos do jogo
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

class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.is_broken = False
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw(self, screen):
        if not self.is_broken:
            pygame.draw.rect(screen, self.color, self.rect)

def create_bricks():
    return [Brick(x * BRICK_WIDTH, y * BRICK_HEIGHT) for x in range(10) for y in range(5)]

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

# Função principal do jogo, mova esta função para cá de runner.py
def start_game(paddle_control):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breakout com CV")

    # Criar objetos do jogo
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()

    # Variáveis do jogo
    running = True
    clock = pygame.time.Clock()
    lives = 2

    # Mostrar a tela inicial
    show_main_screen(screen)

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Pegar a posição do paddle do CV
        paddle_x = paddle_control.get_paddle_position()
        if paddle_x is not None:
            paddle.move(paddle_x)

        # Movimento da bola
        ball.move()
        if ball.rect.colliderect(paddle.rect):
            ball.bounce()

        # Colisão com os tijolos
        for brick in bricks:
            if ball.rect.colliderect(brick.rect) and not brick.is_broken:
                brick.is_broken = True
                ball.bounce()

        # Verificar condição de vitória
        if all(brick.is_broken for brick in bricks):
            screen.fill((0, 0, 0))
            win_text = pygame.font.Font(None, 36).render("Você Venceu!", True, (0, 255, 0))
            screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

        # A bola cai fora da tela
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

        # Desenhar os objetos do jogo
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)

        # Mostrar as vidas restantes
        lives_text = pygame.font.Font(None, 36).render(f"Vidas: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    paddle_control.release()
    pygame.quit()
