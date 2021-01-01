from ast import Str
import pygame

class Button():
  '''
    The purpose of this class is drawing a rectangle on 
    the window that will be used as a button for the program.
  '''
  def __init__(self, x, y, width, height, color, text = "", textColor = (255,255,255)):
    self.x = x
    self.y = y 
    self.width = width
    self.height = height
    self.color = color
    self.text = text
    self.textColor = textColor 

  def drawButton(self, surface, outline = None):
    '''This method will draw the button on the screen'''
    if outline:
      pygame.draw.rect(surface, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))

    pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    if self.text != '': 
      font = pygame.font.SysFont('freesansbold.ttf', 30)
      buttonTxt = font.render(self.text, 1, self.textColor)
      surface.blit(buttonTxt, (self.x + (self.width/2 - buttonTxt.get_width() / 2), self.y + (self.height / 2 - buttonTxt.get_height() / 2)))

  def mouseHover(self, mousePos) -> bool:
    '''This function will check if the mouse is Hovering over the button area'''
    if mousePos[0] > self.x and mousePos[0] < self.x + self.width:
      if mousePos[1] > self.y and mousePos[1] < self.y + self.height:
        return True

    return False
