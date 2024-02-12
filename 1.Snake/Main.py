import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 10
SNAKE_SPEED = 10
MEGA_APPLE_CHANCE = 0.1
MEGA_APPLE_DURATION = 5 * FPS  # 5 seconds

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize pygame
pygame.init()
pygame.display.set_caption("Snake Game")

# Fonts
font = pygame.font.Font(None, 36)

# Functions
def draw_text(surface, text, color, x, y):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def spawn_apple():
    return (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

def draw_grid(surface):
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, (40, 40, 40), rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.speed = SNAKE_SPEED

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.speed = SNAKE_SPEED

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

    def increase_speed(self):
        self.speed += 1

# Apple class
class Apple:
    def __init__(self):
        self.position = spawn_apple()
        self.color = RED

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, BLACK, r, 1)

# MegaApple class
class MegaApple:
    def __init__(self):
        self.position = spawn_apple()
        self.color = BLUE
        self.duration = MEGA_APPLE_DURATION

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, BLACK, r, 1)

# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()
    mega_apple = None

    running = True
    while running:
        screen.fill(WHITE)

        # Event handling
        snake.handle_keys()

        # Snake movement
        snake.move()

        # Check collision with apple
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.score += 1
            snake.increase_speed()
            apple = Apple()
            if random.random() < MEGA_APPLE_CHANCE:
                mega_apple = MegaApple()

        # Check collision with mega apple
        if mega_apple and snake.get_head_position() == mega_apple.position:
            snake.score += 5
            mega_apple = None

        # Draw snake, apple, and mega apple
        snake.draw(screen)
        apple.draw(screen)
        if mega_apple:
            mega_apple.draw(screen)

        # Draw score
        draw_text(screen, f"Score: {snake.score}", BLACK, 10, 10)

        # Update screen
        pygame.display.flip()

        # Control the frame rate
        clock.tick(snake.speed)

if __name__ == "__main__":
    main()
