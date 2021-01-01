import pygame

class ScreenObject():
  def __init__(self, x, y, changeX, changeY, iconPath):
    self.x = x
    self.y = y
    self.changeX = changeX
    self.changeY = changeY
    self.icon = pygame.image.load(iconPath)

  def draw(self, screen, x, y):
    screen.blit(self.icon, (x,y))
