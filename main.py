# Credits
'''
Game Icon -> Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
Spaceship -> Icons made by <a href="https://www.flaticon.com/authors/photo3idea-studio" title="photo3idea_studio">photo3idea_studio</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
Enemy -> Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
'''

import pygame
from pygame import mixer

import random
import math

# Initiates Pygame*
pygame.init()
mixer.init()

# Creates a screen with a width of 800 and a height 600
screen = pygame.display.set_mode((800, 600))

# Controls the game
done = False

# Title and Icon
pygame.display.set_caption('Space Invader Clone')
icon = pygame.image.load('SolarSystemIcon.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('Background.jpg')

# Background Sound
mixer.music.load('MusicForLvl.wav')
mixer.music.play(-1)

# Keeps the score
currentScore = 0

# Score Text
font = pygame.font.Font('freesansbold.ttf', 32)
#Game Over Text
overFont = pygame.font.Font('freesansbold.ttf', 64)

textX = 10
textY = 10

def showScore(x, y):
    score = font.render("Score : " + str(currentScore), True, (255, 255, 255))
    screen.blit(score, (x, y))

def gameOver():
    overText = overFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overText, (200, 250))

# Player
playerIcon = pygame.image.load('spaceship.png')
# These variables control the position of the player on the screen
playerX = 370
playerY = 480
playerX_change = 0

# This function will control the movement of the player
def player(x, y):
    # Blit draws the image on the screen
    screen.blit(playerIcon, (x, y))

# Enemy
enemyIcon = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numEnemies = 6

for i in range(numEnemies):
    enemyIcon.append(pygame.image.load('ufo.png'))
    # These variables control the position of the enemy ship
    enemyX.append(random.randint(5, 729))
    enemyY.append(random.randint(5, 225))
    enemyX_change.append(1.5)
    enemyY_change.append(30)

def enemy(x, y, i):
    screen.blit(enemyIcon[i], (x, y))

# Bullet
bulletIcon = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 5
bulletState = 'ready'

def bullet(x, y):
    global bulletState
    bulletState = 'fire'

    screen.blit(bulletIcon, (x + 16, y + 10))

# Calculate Collinsion
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    return False

# Game Loop
while not done:
    # RGB for the background of the screen
    screen.fill((105, 105, 105, 0.2))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Check if left or right is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                # Avoids bullets from refreshing mid flight
                if bulletState is 'ready':
                    bulletSound = mixer.Sound('151022__bubaproducer__laser-shot-silenced.wav')
                    bulletSound.play()
                    # Get the location of the ship to keep the bullet fixed on x axis
                    bulletX = playerX
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Updating the position of the player
    playerX += playerX_change

    # Keeping the ship within boundaries of x axis in screen
    if playerX > 730:
        playerX = 730
    elif playerX < 5:
        playerX = 5
    # Keeping the ship within boundaries for y axis of the screen
    if playerY > 535:
        playerY = 535
    elif playerY < 5:
        playerY = 5

    # Enemy Movement
    for i in range(numEnemies):
        #Game Over
        if enemyY[i] > 440:
            for j in range(numEnemies):
                enemyY[j] = 2000

            gameOver()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 5:
            enemyX_change[i] = 1.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 730:
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]

        # Check for collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion = mixer.Sound('EnemyKill.wav')
            explosion.play()
            bulletY = 480
            bulletState = 'ready'
            currentScore += 1
            enemyX[i] = random.randint(5, 730)
            enemyY[i] = random.randint(5, 225)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    # If the bullet goes out of bounds 'Load a new bullet'
    if bulletY <= 0:
        bulletY = 480
        bulletState = 'ready'

    # Controls trajectory of bullet
    if bulletState is 'fire':
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)

    # Display Current Score
    showScore(textX, textY)

    # Updates the display*
    pygame.display.update()