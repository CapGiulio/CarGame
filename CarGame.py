import pygame
import random


pygame.init()

# Here I just define and initialize basic stuff for the game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


CAR_WIDTH = 50
CAR_HEIGHT = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Game by Giulio Caputi")

clock = pygame.time.Clock()


def draw_car(x, y):
    pygame.draw.rect(screen, GREEN, [x, y, CAR_WIDTH, CAR_HEIGHT])


def draw_obstacle(obstacle_rect):
    pygame.draw.rect(screen, RED, obstacle_rect)


def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


def display_score(score):
    font = pygame.font.SysFont(None, 35)
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))


def message_display(text):
    small_text = pygame.font.SysFont("comicsansms", 25)
    TextSurf, TextRect = text_objects(text, small_text)
    TextRect.center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()


def wait_for_key(score):
    message_display('You lost :( Press P to play again, or Q to quit')
    display_score(score)  # Display the score even after crashing
    pygame.display.update()  # Update the display to ensure the score is redrawn
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def crash(score):
    wait_for_key(score)


# Up to now everything is quite intuitive
# Now the funny part starts: I define the function to actually play
def run_game():
    x = (SCREEN_WIDTH * 0.45)
    y = (SCREEN_HEIGHT * 0.8)
    x_change = 0

    obstacle_speed = 3
    obstacle_startx = random.randrange(0, SCREEN_WIDTH)
    obstacle_starty = -600
    obstacle_width = random.randrange(10, 100)
    obstacle_height = random.randrange(10, 100)
    score = 0
    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        screen.fill(WHITE)
        draw_car(x, y)

        obstacle_starty += obstacle_speed
        if obstacle_starty > SCREEN_HEIGHT:
            obstacle_starty = 0 - obstacle_height
            obstacle_startx = random.randrange(0, (SCREEN_WIDTH - obstacle_width))
            obstacle_width = random.randrange(10, 101)
            obstacle_height = random.randrange(10, 101)
            score += 10
            obstacle_speed += 0.5 if obstacle_speed < 15 else 0  # Cap the speed increase

        draw_obstacle([obstacle_startx, obstacle_starty, obstacle_width, obstacle_height])

        if y < obstacle_starty + obstacle_height:
            if x + CAR_WIDTH > obstacle_startx and x < obstacle_startx + obstacle_width or x + CAR_WIDTH > obstacle_startx and x < obstacle_startx + obstacle_width:
                crash(score)  # Pass the final score to the crash function
                game_exit = True  # Set game_exit to True to end the game loop

        display_score(score)

        pygame.display.update()
        clock.tick(60)


# This line makes the game start
run_game()
