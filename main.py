from random import choice
import pygame

# Dimensions and grid size settings
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Movement directions
MOVE_RIGHT = (1, 0)
MOVE_LEFT = (-1, 0)
MOVE_DOWN = (0, 1)
MOVE_UP = (0, -1)

SNAKE_SPEED = 20

# Colors
COLOR_BG = (0, 0, 0)
COLOR_BORDER = (153, 102, 204)
COLOR_SNAKE = (0, 255, 0)
COLOR_FOOD = (255, 0, 0)

# Game setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Base class for game objects
class GameObject:
    def __init__(self, position=None, color=None):
        """
        Initialize a game object, the unsung hero of the game's architecture.
        :param position: Starting position (tuple).
        :param color: Appearance in RGB.
        """
        self.position = position if position else (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.color = color

    def draw(self):
        """
        Draw the object on the screen. Override this or suffer my eternal disdain.
        """
        raise NotImplementedError("Subclasses must implement the draw method!")


class Food(GameObject):
    """
    The snack of champions. Appears, disappears, and makes the snake grow.
    """
    def __init__(self):
        super().__init__(color=COLOR_FOOD)
        self.randomize_position()

    def randomize_position(self) -> tuple:
        """
        randomize the position of the apple and return it.
        """
        x = choice(range(0, SCREEN_WIDTH, GRID_SIZE))
        y = choice(range(0, SCREEN_HEIGHT, GRID_SIZE))
        self.position = (x, y)
        return self.position

    def draw(self) -> None:
        """
        display the only one product in snake's world
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, COLOR_BORDER, rect, 1)


class Snake(GameObject):
    """
    the protagonist of this adventure
    """
    def __init__(self):
        super().__init__(color=COLOR_SNAKE)
        self.length = 1
        self.positions = [self.position]
        self.direction = MOVE_RIGHT
        self.next_direction = None
        self.last_position = None

    def update_direction(self) -> None:
        """
        changing direction of the snake
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """
        Guide the snake forward, avoiding self-inflicted doom.
        """
        head_pos = self.get_head_position()
        new_head = (
            (head_pos[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_pos[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        if new_head in self.positions[2:]:
            self.reset()
            return

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last_position = self.positions.pop()

    def draw(self) -> None:
        """
        Render the snake in its full wiggly glory.
        """
        for pos in self.positions[:-1]:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, COLOR_BORDER, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, head_rect)
        pygame.draw.rect(screen, COLOR_BORDER, head_rect, 1)

        if self.last_position:
            last_rect = pygame.Rect(self.last_position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, COLOR_BG, last_rect)

    def get_head_position(self) -> tuple:
        """
        just head position, what u want to find here?
        """
        return self.positions[0]

    def reset(self) -> None:
        """
        fresh start for snake
        """
        # Clear all remaining snake segments from the screen
        for pos in self.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, COLOR_BG, rect)

        # Reset snake properties
        self.length = 1
        self.positions = [self.position]
        self.direction = MOVE_RIGHT
        self.next_direction = None
        self.last_position = None


def handle_keys(snake: Snake) -> None:
    """
    input okey?
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != MOVE_DOWN:
                snake.next_direction = MOVE_UP
            elif event.key == pygame.K_DOWN and snake.direction != MOVE_UP:
                snake.next_direction = MOVE_DOWN
            elif event.key == pygame.K_LEFT and snake.direction != MOVE_RIGHT:
                snake.next_direction = MOVE_LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != MOVE_LEFT:
                snake.next_direction = MOVE_RIGHT


def main():
    """
    START!!!!!!!!!!!!!!!!!!!!
    """
    pygame.init()
    snake = Snake()
    food = Food()

    while True:
        clock.tick(SNAKE_SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == food.position:
            snake.length += 1
            food.randomize_position()

        snake.draw()
        food.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
