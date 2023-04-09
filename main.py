import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 11

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10
# high_score_file = 'high_score.txt'
# try:
#     with open(high_score_file, 'r') as f:
#         high_score = int(f.read())
# except:
#     high_score = 0
# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
    # high_score_text = font.render("High Score: " + str(high_score), True, (255, 255, 255))
    # screen.blit(high_score_text, (x, y + 50))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    restart_text = font.render("Press R to restart", True, (255, 255, 255))
    screen.blit(restart_text, (250, 330))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        explosionSound = mixer.Sound("explosion.wav")
        explosionSound.play()
        return True
    else:
        return False



# Game Loop
running = True
while running:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Move the player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            del enemyX[i]
            del enemyY[i]
            del enemyX_change[i]
            del enemyY_change[i]
            num_of_enemies -= 1
            break

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Restart the game
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        playerX = 370
        playerY = 480
        score_value = 0
        num_of_enemies = 12
        enemyImg = []
        enemyX = []
        enemyY = []
        enemyX_change = []
        enemyY_change = []
        bullet_state = "ready"
        for i in range(num_of_enemies):
            enemyImg.append(pygame.image.load("enemy.png"))
            enemyX.append(random.randint(0, 735))
            enemyY.append(random.randint(50, 150))
            enemyX_change.append(4)
            enemyY_change.append(40)

    # Show the score
    show_score(textX, textY)
    # Draw the player on the screen
    player(playerX, playerY)
    # Draw the enemies on the screen
    for i in range(num_of_enemies):
        enemy(enemyX[i], enemyY[i], i)
    if num_of_enemies == 0:
        win_text = over_font.render("You won!", True, (255, 255, 255))
        screen.blit(win_text, (250, 250))
        restart_text = font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(restart_text, (250, 330))

    # Update the screen
    pygame.display.update()

