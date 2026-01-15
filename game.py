import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600
player_size = 50  # We define this here...
enemy_size = 50
SPEED = 10
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BACKGROUND_COLOR = (0,0,0)

# Load Images
background_image = pygame.image.load("background.png")
player_image = pygame.image.load("player.png")
enemy_image = pygame.image.load("enemy.png")

# Scale images to match your hitboxes
player_image = pygame.transform.scale(player_image, (player_size, player_size))
enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))

player_size = 50
player_pos = [WIDTH/2, HEIGHT-2*player_size]

enemy_size = 50
enemy_list = [] # Start with an empty list

SPEED = 5 # Start a bit slower

screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_over = False
score = 0
clock = pygame.time.Clock()
myFont = pygame.font.SysFont("Arial", 35, bold=True)

def set_level(score, SPEED):
    if score < 20:
        SPEED = 5
    elif score < 40:
        SPEED = 8
    elif score < 60:
        SPEED = 12
    else:
        SPEED = 15
    return SPEED

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        (screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1])))

def update_enemy_positions(enemy_list, score):
    # We iterate through a COPY of the list [:] to avoid index errors when popping
    for idx, enemy_pos in enumerate(enemy_list[:]): 
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(enemy_list.index(enemy_pos))
            score += 1
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x, p_y = player_pos
    e_x, e_y = enemy_pos

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
            return True
    return False

# --- Main Game Loop ---
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if event.key == pygame.K_LEFT and x > 0: # Added boundary check
                x -= player_size
            elif event.key == pygame.K_RIGHT and x < WIDTH - player_size: # Added boundary check
                x += player_size
            player_pos = [x,y]

    screen.blit(background_image, (0, 0))
    screen.blit(player_image, (player_pos[0], player_pos[1]))

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    SPEED = set_level(score, SPEED)

    # Display Score
    label = myFont.render(f"Score: {score}", 1, YELLOW)
    screen.blit(label, (WIDTH-200, HEIGHT-40))

    if collision_check(enemy_list, player_pos):
        game_over = True

    draw_enemies(enemy_list)
    # This "blits" (copies) your image onto the screen
    screen.blit(player_image, (player_pos[0], player_pos[1]))

    clock.tick(30)
    pygame.display.update()

# --- Game Over Screen ---
screen.fill(BACKGROUND_COLOR)
over_label = myFont.render("GAME OVER!", 1, RED)
screen.blit(over_label, (WIDTH/2 - 100, HEIGHT/2))
pygame.display.update()
pygame.time.wait(2000) # Wait 2 seconds before closing
pygame.quit()