import pygame, sys
import os
import random

player_lives = 3  # keep track of lives
score = 0  # keeps track of score
fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb', 'ice_cube2']  # entities in the game

# initialize pygame and create window
WIDTH = 800
HEIGHT = 500
FPS = 12  # controls how often the gameDisplay should refresh

GRAVITY = 1.2        # gravity force (stronger fall)
SPEED_FACTOR = 0.3  # slows movement without changing randint
SPAWN_DELAY = 15    # frames between fruit spawns

spawn_timer = 0

pygame.init()
pygame.display.set_caption('Final fantasy Fruits Game')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))  # setting game display size
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# load and scale background image to fit the screen
bg_img = pygame.image.load('./images/572603.jpg')
background = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))  # scale to window size

font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)
lives_icon = pygame.image.load('images/white_lives.png')  # shows remaining lives


# Generalized structure of the fruit Dictionary
def generate_random_fruits(fruit):
    fruit_path = "images/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x': random.randint(100, 500),      # x position
        'y': HEIGHT,                        # start from bottom of the screen
        'speed_x': random.randint(-10, 10), # horizontal speed (unchanged)
        'speed_y': random.randint(-80, -60),# vertical speed (unchanged)
        'throw': True,                      # fruit is ready to be thrown
        'hit': False,
    }


# Dictionary to hold the data of fruits
data = {}
for fruit in fruits:
    generate_random_fruits(fruit)


# Generic method to draw fonts on the screen
font_name = pygame.font.match_font('comic.ttf')


def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    display.blit(text_surface, text_rect)


# draw players lives
def draw_lives(display, x, y, lives, image):
    for i in range(lives):
        img = pygame.image.load(image)
        img_rect = img.get_rect()
        img_rect.x = int(x + 35 * i)
        img_rect.y = y
        display.blit(img, img_rect)


# show game over display & front display
def show_gameover_screen():
    gameDisplay.blit(background, (0, 0))
    draw_text(gameDisplay, "FINAL FANTASY FRUITS", 90, WIDTH / 2, HEIGHT / 4)
    draw_text(gameDisplay, "Press any key to start", 50, WIDTH / 2, HEIGHT / 2)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False


# Game Loop
first_round = True
game_over = True
game_running = True

while game_running:

    if game_over:
        if first_round:
            show_gameover_screen()
            first_round = False

        game_over = False
        player_lives = 3
        score = 0

        for fruit in fruits:
            generate_random_fruits(fruit)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    gameDisplay.blit(background, (0, 0))  # draw scaled background

    score_text = font.render('Score : ' + str(score), True, WHITE)
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')

    current_position = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    spawn_timer += 1

    for key, value in data.items():
        if value['throw']:

            # movement
            value['x'] += value['speed_x'] * SPEED_FACTOR
            value['y'] += value['speed_y'] * SPEED_FACTOR
            value['speed_y'] += GRAVITY

            # limit fall speed
            if value['speed_y'] > 35:
                value['speed_y'] = 35

            # draw fruit
            if value['y'] <= HEIGHT:
                gameDisplay.blit(value['img'], (value['x'], value['y']))
            else:
                value['throw'] = False

            # mouse collision
            if mouse_pressed[0] and not value['hit']:
                if value['x'] < current_position[0] < value['x'] + 60 and \
                   value['y'] < current_position[1] < value['y'] + 60:

                    value['hit'] = True

                    if key == 'bomb':
                        player_lives -= 3
                        value['img'] = pygame.image.load("images/explosion.png")

                        if player_lives <= 0:
                            show_gameover_screen()
                            game_over = True
                            break
                    else:
                        value['img'] = pygame.image.load("images/half_" + key + ".png")
                        score += 1

        else:
            # controlled spawn timing
            if spawn_timer >= SPAWN_DELAY:
                generate_random_fruits(key)
                spawn_timer = 0

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()



