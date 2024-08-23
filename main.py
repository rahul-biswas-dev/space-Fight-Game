import pygame
import random
import math
from pygame import mixer

# initialise the pygame
pygame.init()
clock = pygame.time.Clock()

# create the screen
screen = pygame.display.set_mode((800, 533))

# background
backgroung = pygame.image.load("assets/back.png")

# backgroung sound
mixer.music.load("assets/space-invaders-classic-arcade-game-116826.mp3")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(r"assets/ufo.png")
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load(r"assets/spaceship.png")
playerX = 370
playerY = 450
playerX_change = 0

# enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemy_img.append(pygame.image.load(r"assets/alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.5)
    enemyY_change.append(40)

# bullet

# ready = you can't see the bullet
# fire = the bullet is currently moving

bullet_img = pygame.image.load(r"assets/bullet.png")
bulletX = 0
bulletY = 450
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textx = 10
texty = 10

# game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("score : " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over_text, (210, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 0, y + 10))


def is_collusion(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:

    # RGB-- RED GREEN BLUE
    screen.fill((0, 0, 0))
    # background image
    screen.blit(backgroung, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handling Keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("assets/laser.wav")
                    bullet_sound.set_volume(0.5)
                    bullet_sound.play()
                    # get the current x coordinate of the spaceship
                    bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking for boundary of spaceship, so it doesn't go out of bound
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # checking for enemy movement
    for i in range(num_of_enemy):

        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]

        # collision
        collision = is_collusion(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("assets/8-bit-kit-explosion-2.wav")
            explosion_sound.set_volume(0.5)
            explosion_sound.play()
            bulletY = 450
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 450
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textx, texty)
    clock.tick(120)
    pygame.display.update()