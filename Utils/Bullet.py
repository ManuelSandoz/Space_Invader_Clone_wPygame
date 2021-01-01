import pygame
import math
from Utils.ScreenObject import ScreenObject

class Bullet(ScreenObject):
  def __init__(self, x, y, changeX, changeY, iconPath, state):
    super().__init__(x, y, changeX, changeY, iconPath)
    self.state = state

  def collision(self, x2, y2) -> bool:
    distance = math.sqrt((math.pow(self.x - x2, 2)) + (math.pow(self.y - y2, 2)))
    if distance < 27:
      return True
    return False

  def drawBullet(self, screen): 
    self.state = 'fire'

    screen.blit(self.icon, (self.x + 16, self.y + 10))

