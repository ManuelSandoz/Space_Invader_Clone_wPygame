# Credits
'''
Game Icon -> Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
Spaceship -> Icons made by <a href="https://www.flaticon.com/authors/photo3idea-studio" title="photo3idea_studio">photo3idea_studio</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
Enemy -> Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
'''

# Modules for game functionalities
import pygame
from pygame import mixer

# Modules for additional functionalities
import random
import math

# Clases for the project
from Utils.Button import Button
from Utils.ScreenObject import ScreenObject

# Initiates Pygame*
pygame.init()
mixer.init()

# Creates a screen with a width of 800 and a height 600
screen = pygame.display.set_mode((800, 600))

# Controls the game
done = False

# Title and Icon
pygame.display.set_caption('Space Invader Clone')
icon = pygame.image.load('Images/SolarSystemIcon.png')
pygame.display.set_icon(icon)

# Loads Background Img
background = pygame.image.load('Images/Background.jpg')

# Background Sound
# mixer.music.load('Sounds/MusicForLvl.wav')
# mixer.music.play(-1)

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

# Buttons for the game over message
replayButton = Button(270, 350, 100, 50, (0,0,0), 'Replay')
quitButton = Button(430, 350, 125, 50, (0,0,0), 'Quit Game')

# Player
# These variables control the position of the player on the screen
playerX = 370
playerY = 480
playerX_change = 0

player = ScreenObject(playerX, playerY, playerX_change, 0, 'Images/spaceship.png')

# Enemy
enemyIcon = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numEnemies = 6

for i in range(numEnemies):
    enemyIcon.append(pygame.image.load('Images/ufo.png'))
    # These variables control the position of the enemy ship
    enemyX.append(random.randint(5, 729))
    enemyY.append(random.randint(5, 225))
    enemyX_change.append(1.5)
    enemyY_change.append(30)

def enemy(x, y, i):
    screen.blit(enemyIcon[i], (x, y))

# Bullet
bulletIcon = pygame.image.load('Images/bullet.png')
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
    # screen.fill((105, 105, 105, 0.2))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # If user clicks on the 'x' close program
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            quit()

        # Check if left or right is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                # Avoids bullets from refreshing mid flight
                if bulletState == 'ready':
                    bulletSound = mixer.Sound('Sounds/bulletSound.wav')
                    bulletSound.play()
                    # Get the location of the ship to keep the bullet fixed on x axis
                    bulletX = playerX
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        
        mousePos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEMOTION:
            if replayButton.mouseHover(mousePos):
                replayButton.color = (255,255,255)
                replayButton.textColor = (0,0,0)
            else:
                replayButton.color = (0,0,0)
                replayButton.textColor = (255,255,255)

            if quitButton.mouseHover(mousePos):
                quitButton.color = (255,255,255)
                quitButton.textColor = (0,0,0)
            else:
                quitButton.color = (0,0,0)
                quitButton.textColor = (255,255,255)
        
        # This cheks if the mouse button is pressed down on a button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if replayButton.mouseHover(mousePos):
                # pass for now
                pass

            if quitButton.mouseHover(mousePos):
                done = True
                pygame.quit()
                quit()


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
        #Check the position of enemies and display game over if necessary. 
        if enemyY[i] > 440:
            for j in range(numEnemies):
                enemyY[j] = 2000

            replayButton.drawButton(screen, (255,255,255))
            quitButton.drawButton(screen, (255,255,255))
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
            explosion = mixer.Sound('Sounds/EnemyDeath.wav')
            explosion.play()
            bulletY = 480
            bulletState = 'ready'
            currentScore += 1
            enemyX[i] = random.randint(5, 730)
            enemyY[i] = random.randint(5, 225)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    # If the bullet goes out of bounds "Load" a new bullet
    if bulletY <= 0:
        bulletY = 480
        bulletState = 'ready'

    # Controls trajectory of bullet
    if bulletState == 'fire':
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Updates the location of the user
    player.draw(screen, playerX, playerY)

    # Display Current Score
    showScore(textX, textY)

    # Updates the display*
    pygame.display.update()