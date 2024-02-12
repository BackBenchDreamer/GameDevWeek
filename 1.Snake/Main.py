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
MAX_SPEED = 20
MEGA_APPLE_CHANCE = 0.1
MEGA_APPLE_DURATION = 5 * FPS  # 5 seconds
FONT_NAME = pygame.font.match_font('arial')

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize pygame
pygame.init()
pygame.display.set_caption("Snake Game")

# Fonts
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Functions
def draw_grid(surface):
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, (40, 40, 40), rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

def spawn_apple(snake):
    while True:
        x = random.randrange(GRID_WIDTH)
        y = random.randrange(GRID_HEIGHT)
        if (x, y) not in snake:
            return (x * GRID_SIZE, y * GRID_SIZE)

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
        if self.speed < MAX_SPEED:
            self.speed += 1

# Apple class
class Apple:
    def __init__(self):
        self.position = spawn_apple([]) # Initialize with empty snake

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, r)
        pygame.draw.rect(surface, BLACK, r, 1)

# MegaApple class
class MegaApple:
    def __init__(self):
        self.position = spawn_apple([])
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

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    main_game(screen, clock, snake, apple, mega_apple)

        screen.fill(BLACK)
        draw_text(screen, "Snake Game", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        start_button_rect = pygame.Rect(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2, 100, 50)
        pygame.draw.rect(screen, GREEN, start_button_rect)
        draw_text(screen, "Start", 36, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10)

        pygame.display.flip()
        clock.tick(FPS)

def main_game(screen, clock, snake, apple, mega_apple):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        snake.handle_keys()
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

        # Draw everything
        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        if mega_apple:
            mega_apple.draw(screen)
        draw_text(screen, f"Score: {snake.score}", 18, 100, 10)
        pygame.display.flip()
        clock.tick(snake.speed)

if __name__ == "__main__":
    main()
