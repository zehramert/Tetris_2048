import lib.stddraw as stddraw  # used for displaying the game grid
from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing
import copy as cp
from player import Player

# A class for modeling the game grid
class GameGrid:
   # A constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w):
      # Create player
      self.player = Player()
      # Initialize score
      self.score = 0
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create a tile matrix to store the tiles locked on the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # create the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      # create the next tetromino that will be move on the game grid
      self.next_tetromino = None
      # the game_over flag shows whether the game is over or not
      self.game_over = False
      # set the color used for the empty grid cells
      self.empty_cell_color = Color(206, 195, 181)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(187, 173, 160)
      self.boundary_color = Color(132, 122, 112)
      # thickness values used for the grid lines and the grid boundaries
      self.line_thickness = 0.002
      self.box_thickness = 5 * self.line_thickness


   # A method for displaying the game grid
   def display(self):
      # clear the background to empty_cell_color
      stddraw.clear(self.empty_cell_color)
      # draw the game grid
      self.draw_grid()
      # draw the score
      self.display_Score()

      # Pause Game button
      button_width = 2
      button_height = 1
      button_x = 13.5
      button_y = 10.5
      button_color = Color(237, 224, 200)
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(button_x, button_y, button_width, button_height)
      stddraw.setPenColor(Color(255, 255, 255))
      stddraw.setFontFamily("Arial")
      stddraw.setFontSize(20)
      stddraw.text(button_x + button_width / 2, button_y + button_height / 2, "Pause")

      if stddraw.mousePressed():
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY() #get the coordinates of mouse that has been clicked
         # check if these coordinates are inside the pause button
         if mouse_x >= 13.5 and mouse_x <= 14.5:
            if mouse_y >= 10.5 and mouse_y <= 11.5:
               self.pause_screen(self.grid_width, self.grid_height)



      # draw the current/active tetromino if it is not None
      # (the case when the game grid is updated)
      if self.current_tetromino is not None:
         self.current_tetromino.draw()
      # Draw the next tetromino next to the game grid if it is not None
      if self.next_tetromino is not None:
         self.next_tetromino.draw_outside()
      # draw a box around the game grid
      self.draw_boundaries()
      # show the resulting drawing with a pause duration according to difficulty level
      if (self.player.getDiff() == 0):
         stddraw.show(250)
      if (self.player.getDiff() == 1):
         stddraw.show(200)
      if (self.player.getDiff() == 2):
         stddraw.show(125)





   # A method for drawing the cells and the lines of the game grid

   def draw_grid(self):
      # for each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            # if the current grid cell is occupied by a tile
            if self.tile_matrix[row][col] is not None:
               # draw this tile
               self.tile_matrix[row][col].draw(Point(col, row))
      # draw the inner lines of the game grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)

      stddraw.setFontSize(25)
      stddraw.setPenColor(Color(255, 255, 255))
      stddraw.text(14.5, 5.5, "NEXT:")

      stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method for drawing the boundaries around the game grid
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness)
      # the coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method used checking whether the grid cell with the given row and column
   # indexes is occupied by a tile or not (i.e., empty)
   def is_occupied(self, row, col):
      # considering the newly entered tetrominoes to the game grid that may
      # have tiles with position.y >= grid_height
      if not self.is_inside(row, col):
         return False  # the cell is not occupied as it is outside the grid
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] is not None

   # A method for checking whether the cell with the given row and col indexes
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   # Method that locks the tiles of the landed tetromino on the game grid while
   # checking if the game is over due to having tiles above the topmost grid row.
   # The method returns True when the game is over and False otherwise.
   def update_grid(self, tiles_to_lock, blc_position):
      # necessary for the display method to stop displaying the tetromino
      self.current_tetromino = None
      # lock the tiles of the current tetromino (tiles_to_lock) on the game grid
      n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
      for col in range(n_cols):
         for row in range(n_rows):
            # place each tile onto the game grid
            if tiles_to_lock[row][col] is not None:
               # compute the position of the tile on the game grid
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               # the game is over if any placed tile is above the game grid
               else:
                  self.game_over = True
      # return the game_over flag
      return self.game_over

   def clear_tiles(self):
      row = 0
      total_score = 0
      while (row < self.grid_height):
         # check if the row is full
         if all(self.tile_matrix[row]):
            total_score += sum(element.number for element in self.tile_matrix[row])
            # remove the row from the game grid
            self.tile_matrix = np.delete(self.tile_matrix, row, 0)
            # add an empty row to the game grid
            self.tile_matrix = np.insert(self.tile_matrix, -1, None, 0)
         else:
            row += 1
      self.score += total_score

   # draws the ghost tetromino on the game grid
   def ghost_tetromino(self):
      # the ghost tetromino is the same as the current tetromino, but with a
      # different color
      ghost_tetromino = cp.deepcopy(self.current_tetromino)
      while ghost_tetromino.can_be_moved("down", self):
         ghost_tetromino.move("down", self)
      ghost_tetromino.draw(True)

   # Takes list of free tiles and moves them one row down
   def move_free_tiles(self, free_tiles):
      for row in range(self.grid_height):  # does not contain the bottommost row
         for col in range(self.grid_width):
            if free_tiles[row][col]:
               free_tile_copy = cp.deepcopy(self.tile_matrix[row][col])
               self.tile_matrix[row - 1][col] = free_tile_copy
               dx, dy = 0, -1  # change of the position in x and y directions
               self.tile_matrix[row - 1][col].move(dx, dy)
               self.tile_matrix[row][col] = None

   # Displays the score on the top right of the main game screen
   def display_Score(self):
      stddraw.setPenRadius(150)
      stddraw.setPenColor(Color(255, 255, 255))
      text_to_display = "SCORE: " + str(self.score)
      stddraw.text(14.5, 16.5, text_to_display)
      high_score_text = "HIGH SCORE: " + str(self.player.getHighScore())
      stddraw.text(14.5, 13.5, high_score_text)

      # return the value of the game_over flag
      return self.game_over


   def pause_screen(self, grid_width, grid_height):
      background_color = Color(42, 69, 99)
      button_color = Color(25, 255, 228)
      text_color = Color(31, 160, 239)
      button_width = 5
      button_height = 2
      continue_button_center_x = grid_width / 2 + 3
      continue_button_center_y = grid_height / 2 + 3
      exit_button_center_x = grid_width / 2 + 3
      exit_button_center_y = grid_height / 2 - 3

      # Draw the pause menu background
      stddraw.clear(background_color)

      # Draw the "Continue" button
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(continue_button_center_x - button_width / 2, continue_button_center_y - button_height / 2,
                           button_width, button_height)
      stddraw.setPenColor(text_color)
      stddraw.text(continue_button_center_x, continue_button_center_y, "Continue")

      # Draw the "Exit" button
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(exit_button_center_x - button_width / 2, exit_button_center_y - button_height / 2,
                           button_width, button_height)
      stddraw.setPenColor(text_color)
      stddraw.text(exit_button_center_x, exit_button_center_y, "Exit")

      # Display everything drawn to the screen
      stddraw.show()

      # Wait for user interaction
      while True:
         if stddraw.mousePressed():
            mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
            # Check if "Continue" button is clicked
            if (continue_button_center_x - button_width / 2 <= mouse_x <= continue_button_center_x + button_width / 2) and \
                  (
                         continue_button_center_y - button_height / 2 <= mouse_y <= continue_button_center_y + button_height / 2):
               break  # Exit the pause screen and resume the game
            # Check if "Exit" button is clicked
            if (exit_button_center_x - button_width / 2 <= mouse_x <= exit_button_center_x + button_width / 2) and \
                 (exit_button_center_y - button_height / 2 <= mouse_y <= exit_button_center_y + button_height / 2):
               self.game_over = True  # Set the game to end
               break  # Exit the pause screen



