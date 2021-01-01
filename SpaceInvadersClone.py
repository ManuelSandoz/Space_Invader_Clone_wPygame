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
from Utils.Bullet import Bullet

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

# Background Sound (Uncomment line 40-41 for background music)
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
player = ScreenObject(370, 480, 0, 0, 'Images/spaceship.png')

# Enemy
numEnemies = 6
enemies = []

for i in range(numEnemies):
    enemies.append(ScreenObject(
        random.randint(5, 729),
        random.randint(5, 225),
        1.5,
        30,
        'Images/ufo.png'
    ))

# Bullet
bullet = Bullet(0, 480, 0, 5, 'Images/bullet.png', 'ready')

# Game Loop
while not done:
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
                player.changeX = -4
            if event.key == pygame.K_RIGHT:
                player.changeX = 4
            if event.key == pygame.K_SPACE:
                # Avoids bullets from refreshing mid flight
                if bullet.state == 'ready':
                    bulletSound = mixer.Sound('Sounds/bulletSound.wav')
                    bulletSound.play()
                    # Get the location of the ship to keep the bullet fixed on x axis
                    bullet.x = player.x
                    bullet.drawBullet(screen)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.changeX = 0
        
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
    player.x += player.changeX

    # Keeping the ship within boundaries of x axis in screen
    if player.x > 730:
        player.x = 730
    elif player.x < 5:
        player.x = 5
    # Keeping the ship within boundaries for y axis of the screen (This will be used when the player gets vert movement)
    # if player.y > 535:
    #     player.y = 535
    # elif player.y < 5:
    #     player.y = 5

    # Enemy Movement
    for i in range(numEnemies):
        #Check the position of enemies and display game over if necessary. 
        if enemies[i].y > 440:
            for j in range(numEnemies):
                enemies[j].y = 2000

            replayButton.drawButton(screen, (255,255,255))
            quitButton.drawButton(screen, (255,255,255))
            gameOver()
            break

        enemies[i].x += enemies[i].changeX
        if enemies[i].x <= 5:
            enemies[i].changeX = 1.5
            enemies[i].y += enemies[i].changeY
        elif enemies[i].x >= 730:
            enemies[i].changeX = -1.5
            enemies[i].y += enemies[i].changeY

        # Check for collision
        collision = bullet.collision(enemies[i].x, enemies[i].y)
        if collision:
            explosion = mixer.Sound('Sounds/EnemyDeath.wav')
            explosion.play()
            bullet.y = 480
            bullet.state = 'ready'
            currentScore += 1
            enemies[i].x = random.randint(5, 730)
            enemies[i].y = random.randint(5, 225)

        enemies[i].draw(screen)

    # Bullet Movement
    # If the bullet goes out of bounds "Load" a new bullet
    if bullet.y <= 0:
        bullet.y = 480
        bullet.state = 'ready'

    # Controls trajectory of bullet
    if bullet.state == 'fire':
        bullet.drawBullet(screen)
        bullet.y -= bullet.changeY

    # Updates the location of the user
    player.draw(screen)

    # Display Current Score
    showScore(textX, textY)

    # Updates the display*
    pygame.display.update()