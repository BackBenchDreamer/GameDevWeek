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
FONT_NAME = pygame.font.match_font('Comic Sans MS')

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize pygame
pygame.init()
pygame.display.set_caption("Snake Game")

# Fonts
def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, color)
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
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.turn(UP)
        elif keys[pygame.K_DOWN]:
            self.turn(DOWN)
        elif keys[pygame.K_LEFT]:
            self.turn(LEFT)
        elif keys[pygame.K_RIGHT]:
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
    high_score = 0

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    snake.reset()
                    main_game(screen, clock, snake, apple, mega_apple, high_score)

        screen.fill(BLACK)
        draw_text(screen, "Snake Game", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        start_button_rect = pygame.Rect(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2, 100, 50)
        pygame.draw.rect(screen, GREEN, start_button_rect)
        draw_text(screen, "Start", 36, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10)

        # Display high score
        draw_text(screen, f"High Score: {high_score}", 18, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)

        pygame.display.flip()
        clock.tick(FPS)

def main_game(screen, clock, snake, apple, mega_apple, high_score):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        snake.handle_keys()
        if not snake.move():
            defeat_screen(screen, clock, snake, high_score)
            return  # Exit the game loop

        # Check collision with apple
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.score += 1
            if snake.score > high_score:
                high_score = snake.score
            snake.increase_speed()
            apple = Apple()
            if random.random() < MEGA_APPLE_CHANCE:
                mega_apple = MegaApple()

        # Check collision with mega apple
        if mega_apple and snake.get_head_position() == mega_apple.position:
            snake.score += 5
            if snake.score > high_score:
                high_score = snake.score
            mega_apple = None

        # Check collision with self
        if snake.get_head_position() in snake.positions[1:]:
            defeat_screen(screen, clock, snake, high_score)
            return  # Exit the game loop

        # Draw everything
        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        if mega_apple:
            mega_apple.draw(screen)
        draw_text(screen, f"Score: {snake.score}", 18, 100, 10)
        draw_text(screen, f"High Score: {high_score}", 18, SCREEN_WIDTH - 100, 10)
        pygame.display.flip()
        clock.tick(snake.speed)

def defeat_screen(screen, clock, snake, high_score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    return  # Return to main_game loop
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        draw_text(screen, "Game Over!", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        draw_text(screen, f"Score: {snake.score}", 36, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        draw_text(screen, "Click to restart", 24, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        draw_text(screen, "or", 24, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4 + 30)
        draw_text(screen, "Quit", 24, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4 + 60)

        restart_button_rect = pygame.Rect(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT * 3 / 4, 100, 30)
        quit_button_rect = pygame.Rect(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT * 3 / 4 + 60, 100, 30)
        pygame.draw.rect(screen, GREEN, restart_button_rect, 2)
        pygame.draw.rect(screen, GREEN, quit_button_rect, 2)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
    