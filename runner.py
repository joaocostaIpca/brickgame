import pygame
from breaker import Paddle, Ball, Brick, create_bricks, show_main_screen, SCREEN_WIDTH, SCREEN_HEIGHT
from main import PaddleControl

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breakout with CV")

    # Create game objects
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()

    # Initialize computer vision
    paddle_control = PaddleControl(SCREEN_WIDTH)

    # Game variables
    running = True
    clock = pygame.time.Clock()
    lives = 2

    # Show the main screen
    show_main_screen(screen)

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get paddle position from CV
        paddle_x = paddle_control.get_paddle_position()
        if paddle_x is not None:
            paddle.move(paddle_x)

        # Ball movement
        ball.move()
        if ball.rect.colliderect(paddle.rect):
            ball.bounce()

        # Brick collision
        for brick in bricks:
            if ball.rect.colliderect(brick.rect) and not brick.is_broken:
                brick.is_broken = True
                ball.bounce()

        # Check win condition
        if all(brick.is_broken for brick in bricks):
            screen.fill((0, 0, 0))
            win_text = pygame.font.Font(None, 36).render("You Win!", True, (0, 255, 0))
            screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

        # Ball falls below screen
        if ball.rect.y > SCREEN_HEIGHT:
            lives -= 1
            if lives > 0:
                ball = Ball()
            else:
                screen.fill((0, 0, 0))
                game_over_text = pygame.font.Font(None, 36).render("Game Over!", True, (255, 0, 0))
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.delay(2000)
                running = False

        # Draw game objects
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)

        # Display lives
        lives_text = pygame.font.Font(None, 36).render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    paddle_control.release()
    pygame.quit()

if __name__ == "__main__":
    main()
