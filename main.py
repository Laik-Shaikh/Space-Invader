# background image 800*600
# icon 16*16
# players 32*32

import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# create a new window in pygame
screen = pygame.display.set_mode((800, 600))

# chaining title and icon of screen
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('space.png')
pygame.display.set_icon(icon)

# Background Image
background = pygame.image.load('bg.jpg')

# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Adding Player(as a image)
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 478
playerX_change = 0

# Adding Multiple Enemy (as a image)
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 478
bulletX_change = 0
bulletY_change = 1.5
bullet_state = "ready"

# Score
score = 0
scoreX = 10
scoreY = 10

# Score Font
font = pygame.font.Font('freesansbold.ttf', 32)

# Game Over Font
over_font = pygame.font.Font('freesansbold.ttf', 64)

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    scoredis = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(scoredis, (x, y))

def game_over_text():
    game_over = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over, (200, 250))


# main game loop
running = True
while running:

    # background color of screen
    screen.fill((11, 12, 13))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # move spaceship on pressing the key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.8
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.8
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 478
        bullet_state = "ready"

    if bullet_state == "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Multiple enemies
    for i in range(no_of_enemies):
        enemyX[i] += enemyX_change[i]

        if enemyY[i] > 438:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # collision with enemy
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 478
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(scoreX, scoreY)

    pygame.display.update()
