# Modules for game functionalities
import pygame
from pygame import mixer

# Modules for additional functionalities
import random

# Clases for the project
from Utils.Button import Button
from Utils.ScreenObject import ScreenObject
from Utils.Bullet import Bullet

# Initiates Pygame*
pygame.init()
mixer.init()

# Creates a screen with a width of 800 and a height 600
screen = pygame.display.set_mode((800, 600))

# Load Background, Set window title and icon
background = pygame.image.load('Images/Background.jpg')
pygame.display.set_caption('Space Invader Clone')
icon = pygame.image.load('Images/SolarSystemIcon.png')
pygame.display.set_icon(icon)

# Background Sound (Uncomment line 37-38 for background music)
# mixer.music.load('Sounds/MusicForLvl.wav')
# mixer.music.play(-1)

# Keeps the score
currentScore = 0

# Controls the game
done = False

# Fonts for score and Game Over message
scoreFont = pygame.font.Font('freesansbold.ttf', 32)
gameOverFont = pygame.font.Font('freesansbold.ttf', 64)

# Buttons for the game over message
replayButton = Button(270, 350, 100, 50, (0, 0, 0), 'Replay')
quitButton = Button(430, 350, 125, 50, (0, 0, 0), 'Quit Game')

#  Create Player
player = ScreenObject(370, 480, 0, 0, 'Images/spaceship.png')

# Create Enemies
numEnemies = 6
enemies = []

for i in range(numEnemies):
  enemies.append(ScreenObject(
    random.randint(5, 729)
  , random.randint(5, 225)
  , 1.5
  , 30
  , 'Images/ufo.png'
  ))

# Create Bullet
bullet = Bullet(0, 480, 0, 5, 'Images/bullet.png', 'ready')

def displayText(surface, font, message, messageColor, location):
  """
  This function will blit a message on the screen when called

  Args:

      surface (pygame.display): This is the screen in which the message will be rendered
      
      font (pygame.font): Object containing the font and the size for the message to be displayed
      
      message (string): String containing the message to be displayed
      
      messageColor (int touple): Touple containing the RGB value for the color of the text
      
      location (int touple): Touple containing the coordinates for in which the message will be displayed (x, y)
  """  
  text = font.render(message, True, messageColor)
  surface.blit(text, location)

def gameOver():
  displayText(screen, gameOverFont, 'GAME OVER', (255,255,255), (200, 250))
  replayButton.drawButton(screen, (255, 255, 255))
  quitButton.drawButton(screen, (255, 255, 255))

def resetGame():
  global currentScore
  currentScore = 0
  for i in range(numEnemies):
    enemies[i].x = random.randint(5, 729)
    enemies[i].y = random.randint(5, 225)
  

# Game Loop
while not done:
  pygame.time.delay(5)
  # Set Background Image
  screen.blit(background, (0, 0))

  # Get the event queue and check if any action needs to occur  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True

    # Check for player movement
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        player.changeX = -4
      if event.key == pygame.K_RIGHT:
        player.changeX = 4
      if event.key == pygame.K_SPACE:
        # Avoids bullets from refreshing mid flight
        if bullet.state == 'ready':
          mixer.Sound('Sounds/bulletSound.wav').play()
          # Get the location of the ship to keep the bullet fixed on x-axis
          bullet.x = player.x
          bullet.drawBullet(screen)

    # This keeps the enemy from moving infinitely when a key is pressed
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        player.changeX = 0

    # Tracking the mouse movement to make the buttons work
    mousePos = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEMOTION:
      if replayButton.mouseHover(mousePos):
        replayButton.color = (255, 255, 255)
        replayButton.textColor = (0, 0, 0)
      else:
        replayButton.color = (0, 0, 0)
        replayButton.textColor = (255, 255, 255)

      if quitButton.mouseHover(mousePos):
        quitButton.color = (255, 255, 255)
        quitButton.textColor = (0, 0, 0)
      else:
        quitButton.color = (0, 0, 0)
        quitButton.textColor = (255, 255, 255)

    # Check if a button is clicked
    if event.type == pygame.MOUSEBUTTONDOWN:
      if replayButton.mouseHover(mousePos):
        resetGame()

      if quitButton.mouseHover(mousePos):
        done = True

  # Updates the position of the player
  player.x += player.changeX

  # Keeps the player within the game boundaries
  if player.x > 730:
    player.x = 730
  elif player.x < 5:
    player.x = 5

  # Enemy Movement
  for i in range(numEnemies):
    # Check the position of enemies and display game over if necessary.
    if enemies[i].y > 440:
      for j in range(numEnemies):
        enemies[j].y = 700 # <-- pretty sure there is a better way to achieve this effect
        gameOver()
      break

    enemies[i].x += enemies[i].changeX
    if enemies[i].x <= 5 and enemies[i].y <= 700:
      enemies[i].changeX = 1.5
      enemies[i].y += enemies[i].changeY
    elif enemies[i].x >= 730 and enemies[i].y <= 700:
      enemies[i].changeX = -1.5
      enemies[i].y += enemies[i].changeY

    # Check for a collision between bullet and enemies
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
  displayText(screen, scoreFont, 'Score : ' + str(currentScore), (255,255,255), (10,10))

  # Updates the display*
  pygame.display.update()

# Finish and exit game
pygame.quit()
quit()
