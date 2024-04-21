import lib.stddraw as stddraw  # used for drawing the tiles to display them
from lib.color import Color  # used for coloring the tiles
import random as rd
from point import Point


# A class for modeling numbered tiles as in 2048
class Tile:
   # Class variables shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.002
   # font family and font size used for displaying the tile number
   font_family, font_size = "Arial", 14

   # A constructor that creates a tile with 2 or 4 (with 50% probability) as the number on it
   def __init__(self):

      # set the number on this tile
      if (rd.random() < 0.5):
         self.number = 2
      else:
         self.number = 4
      # set the colors of this tile


      if (self.number == 2):
         self.background_color = Color(238, 228, 218) # background (tile) color
         self.foreground_color = Color(138, 129, 120)  # foreground (number) color
      elif (self.number == 4):
         self.background_color = Color(236, 224, 200)
         self.foreground_color = Color(138, 129, 120)
      else:
         self.background_color = Color(236, 224, 200)
         self.foreground_color = Color(138, 129, 120)
      self.box_color = Color(156, 146, 136) # box (boundary) color

      self.position = Point()
   def move(self, dx, dy):

      self.position.x += dx
      self.position.y += dy





   # A method for drawing this tile at a given position with a given length
   def draw(self, position, length=1):  # length defaults to 1
      # draw the tile as a filled square
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(position.x, position.y, length / 2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.text(position.x, position.y, str(self.number))

   # Setter for number property




   def setNumber(self, number):
      self.number = number
      # Numara değiştirildiğinde background_color ve foreground_color değişkenlerinin de değiştirilmesi gerekiyor bu metod içinde.

   # Getter for number property
   def getNumber(self):
      return self.number
