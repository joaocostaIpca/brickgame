# main.py
import pygame
import cv2
import numpy as np
from breaker import Paddle, Ball, Brick, create_bricks, show_main_screen, SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize pygame and create game objects
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout")

# Fonts for displaying lives and game over
small_font = pygame.font.Font(None, 36)

# Create game objects
paddle = Paddle()
ball = Ball()
bricks = create_bricks()

# OpenCV setup
cap = cv2.VideoCapture(0)
lower_red1 = np.array([0, 120, 70], dtype=np.uint8)
upper_red1 = np.array([10, 255, 255], dtype=np.uint8)
lower_red2 = np.array([170, 120, 70], dtype=np.uint8)
upper_red2 = np.array([180, 255, 255], dtype=np.uint8)

# Game loop variables
running = True
clock = pygame.time.Clock()
lives = 2  # Starting lives

# Show main screen before starting the game
show_main_screen(screen)

while running:
    screen.fill((0, 0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture video")
        break

    frame = cv2.flip(frame, 1)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)


 #Morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    red_mask = cv2.erode(red_mask, kernel, iterations=2)
    red_mask = cv2.dilate(red_mask, kernel, iterations=2)
    red_mask = cv2.GaussianBlur(red_mask, (3, 3), 0)

    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        object_center_x = x + w // 2
        frame_width = frame.shape[1]
        normalized_x = object_center_x / frame_width
        paddle_x = int(normalized_x * SCREEN_WIDTH)
        paddle.move(paddle_x)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Camera Feed", frame)
    cv2.imshow("Red Object Mask", red_mask)

    # Ball movement
    ball.move()
    if ball.rect.colliderect(paddle.rect):
        ball.bounce()

    # Ball collision with bricks
    for brick in bricks:
        if ball.rect.colliderect(brick.rect) and not brick.is_broken:
            brick.is_broken = True
            ball.bounce()

    # Ball goes out of bounds
    if ball.rect.y > SCREEN_HEIGHT:
        lives -= 1
        if lives > 0:
            ball = Ball()  # Reset ball position
        else:
            screen.fill((0, 0, 0))
            game_over_text = small_font.render("Game Over!", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

    # Draw everything
    paddle.draw(screen)
    ball.draw(screen)
    for brick in bricks:
        brick.draw(screen)

    # Display lives count
    lives_text = small_font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
