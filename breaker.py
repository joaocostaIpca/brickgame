import pygame
import random
import cv2
import numpy as np

# Initialize pygame
pygame.init()

# Game dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_RADIUS = 10
BRICK_WIDTH = 75
BRICK_HEIGHT = 30

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout")

# Paddle class
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

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

# Ball class
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

    def draw(self):
        pygame.draw.circle(screen, RED, (self.rect.x + BALL_RADIUS, self.rect.y + BALL_RADIUS), BALL_RADIUS)

# Brick class
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.is_broken = False

    def draw(self):
        if not self.is_broken:
            pygame.draw.rect(screen, RED, self.rect)

# Create game objects
paddle = Paddle()
ball = Ball()
bricks = [Brick(x * BRICK_WIDTH, y * BRICK_HEIGHT) for x in range(10) for y in range(5)]

# OpenCV setup
cap = cv2.VideoCapture(0)

# Threshold ranges for detecting red in HSV
lower_red1 = np.array([0, 120, 70], dtype=np.uint8)    # Lower bound for red (0-10 hue range)
upper_red1 = np.array([10, 255, 255], dtype=np.uint8)
lower_red2 = np.array([170, 120, 70], dtype=np.uint8)  # Upper bound for red (170-180 hue range)
upper_red2 = np.array([180, 255, 255], dtype=np.uint8)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Event handling for pygame (Exit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture video")
        break

    # Flip frame for mirror effect
    frame = cv2.flip(frame, 1)

    # Convert the frame to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Apply the red color mask for both low and high ranges of red
    mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # Morphological transformations to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    red_mask = cv2.erode(red_mask, kernel, iterations=2)
    red_mask = cv2.dilate(red_mask, kernel, iterations=2)

    # Blur the mask to smooth the edges
    red_mask = cv2.GaussianBlur(red_mask, (3, 3), 0)

    # Find contours in the red mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If any contours are found, use the largest one to control the paddle
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        object_center_x = x + w // 2

        # Map the red object's x-position to the paddle's movement
        frame_width = frame.shape[1]
        normalized_x = object_center_x / frame_width  # Normalize position to [0, 1]

        # Map normalized x position to paddle's screen range
        paddle_x = int(normalized_x * SCREEN_WIDTH)
        paddle.move(paddle_x)

        # Draw the bounding box around the detected red object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the camera feed and the red mask
    cv2.imshow("Camera Feed", frame)
    cv2.imshow("Red Object Mask", red_mask)

    # Ball movement
    ball.move()

    # Ball collision with paddle
    if ball.rect.colliderect(paddle.rect):
        ball.bounce()

    # Ball collision with bricks
    for brick in bricks:
        if ball.rect.colliderect(brick.rect) and not brick.is_broken:
            brick.is_broken = True
            ball.bounce()

    # Game over condition
    if ball.rect.y > SCREEN_HEIGHT:
        print("Game Over!")
        running = False

    # Draw everything
    paddle.draw()
    ball.draw()
    for brick in bricks:
        brick.draw()

    pygame.display.flip()
    clock.tick(60)

    # Exit OpenCV display with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.quit()
