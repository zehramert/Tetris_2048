################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################


import lib.stddraw as stddraw  # for creating an animation with user interactions
import tile
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types (shapes)
import numpy as np
from point import Point # used for tile positions
from tile import Tile  # used for modeling each tile on the tetrominoes

# The main function where this program starts execution
def start():
   # set the dimensions of the game grid
   grid_h, grid_w = 20, 12
   # set the extra part's width right next to the grid
   extra_w = 6
   # set the size of the drawing canvas (the displayed window)
   canvas_h, canvas_w = 40 * grid_h, 40 * (grid_w + extra_w)
   stddraw.setCanvasSize(canvas_w, canvas_h)
   # set the scale of the coordinate system for the drawing canvas
   stddraw.setXscale(-0.5, (grid_w + extra_w) - 0.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)

   # set the game grid dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w
   # create the game grid
   grid = GameGrid(grid_h, grid_w)
   # Creating the first and next tetromino and assigning them to appropriate variables
   current_tetromino = create_tetromino()
   next_tetromino = create_tetromino()
   grid.current_tetromino = current_tetromino
   grid.next_tetromino = next_tetromino

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   display_game_menu(grid_h, grid_w, grid.player)

   # the main game loop
   while True:
      # check for any user interaction via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
         # if the left arrow key has been pressed
         if key_typed == "left":
            # move the active tetromino left by one
            current_tetromino.move(key_typed, grid)
         # if the right arrow key has been pressed
         elif key_typed == "right":
            # move the active tetromino right by one
            current_tetromino.move(key_typed, grid)
         # if the down arrow key has been pressed
         elif key_typed == "down":
            # move the active tetromino down by one
            # (soft drop: causes the tetromino to fall down faster)
            current_tetromino.move(key_typed, grid)
         elif key_typed == "r" or key_typed == "up":
            # Rotates the tetromino when R key or up key pressed
            current_tetromino.rotate(grid)
         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

      # move the active tetromino down by one at each iteration (auto fall)
      success = current_tetromino.move("down", grid)
      # lock the active tetromino onto the grid when it cannot go down anymore


      if not success:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles, pos)
         # end the main game loop if the game is over



         if game_over:
            break


         merge = apply_merge(grid)
         if merge == True:
            print("merge applied")

         grid.clear_tiles()
         # Assigning the next tetromino to current tetromino to be able to draw it on the game grid
         current_tetromino = grid.next_tetromino
         grid.current_tetromino = current_tetromino
         # Modifying next_tetromino with a new random tetromino
         grid.next_tetromino = create_tetromino()




      # display the game grid with the current tetromino
      grid.display()


   # Updating high score after game is over
   if (grid.score > grid.player.getHighScore()):
      grid.player.setHighScore(grid.score)
   # Updating save file
   grid.player.updateOnClose()
   # print a message on the console when the game is over
   print("Game over")


# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
   # the type (shape) of the tetromino is determined randomly
   tetromino_types = ['I', 'O', 'Z', 'L', 'J', 'S', 'T']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

# A function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width, player):
   # the colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background drawing canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # compute the path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # the coordinates to display the image centered horizontally
   img_center_x, img_center_y = (grid_width + 6 - 1) / 2, grid_height - 7 # +6 is extra part's width
   # the image is modeled by using the Picture class
   image_to_display = Picture(img_file)
   # add the image to the drawing canvas
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # the dimensions for the start game button
   button_w, button_h = grid_width - 1.5, 2
   # the coordinates of the bottom left corner for the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # add the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # add the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Click Here to Start the Game"
   stddraw.text(img_center_x, 5, text_to_display)
   # Settings Button
   s_button_w, s_button_h = 2, 2
   s_button_blc_x, s_button_blc_y = img_center_x - s_button_w / 2, 1
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(s_button_blc_x, s_button_blc_y, s_button_w, s_button_h)
   stddraw.setPenColor(text_color)
   stddraw.text(img_center_x, 2, "Settings")
   # the user interaction loop for the simple menu
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the start game button
      if stddraw.mousePressed():
         # get the coordinates of the most recent location at which the mouse
         # has been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the settings button
         if mouse_x >= s_button_blc_x and mouse_x <= s_button_blc_x + s_button_w:
            if mouse_y >= s_button_blc_y and mouse_y <= s_button_blc_y + s_button_h:
               display_settings_menu(grid_height, grid_width, player) # Opens the settings page
               break
         # check if these coordinates are inside the start button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break  # break the loop to end the method and start the game

# A function for displaying a settings menu before starting the game
def display_settings_menu(grid_height, grid_width, player):
   # the colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   while True:
      # clear the background drawing canvas to background_color
      stddraw.clear(background_color)
      img_center_x, img_center_y = (grid_width + 6 - 1) / 2, grid_height - 7 # +6 is extra part's width
      # Volume Text
      stddraw.setPenColor(Color(0, 0, 0))
      stddraw.text(img_center_x - 6, 15, "Music Volume")
      # Increase Button
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(img_center_x + 7, 14.7, 0.5, 0.5)
      stddraw.setPenColor(Color(0, 0, 0))
      stddraw.text(img_center_x + 7.25, 15, "+")
      # Decrease Button
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(img_center_x + 5, 14.7, 0.5, 0.5)
      stddraw.setPenColor(Color(0, 0, 0))
      stddraw.text(img_center_x + 5.25, 15, "-")
      # Music Text
      stddraw.text(img_center_x - 6, 13, "Music")
      # Difficulty Text
      stddraw.text(img_center_x - 6, 11, "Difficulty")
      # Difficulty Level Text
      difficulty_level_text = ""
      if player.getDiff() == 0:
         difficulty_level_text = "Easy"
      elif player.getDiff() == 1:
         difficulty_level_text = "Normal"
      elif player.getDiff() == 2:
         difficulty_level_text = "Hard"
      stddraw.setPenColor(button_color)
      stddraw.text(img_center_x + 6.2, 11, difficulty_level_text)
      # Difficulty Right
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(img_center_x + 7.5, 10.7, 0.5, 0.5)
      stddraw.setPenColor(Color(0, 0, 0))
      stddraw.text(img_center_x + 7.75, 11, "->")
      # Difficulty Left
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(img_center_x + 4.5, 10.7, 0.5, 0.5)
      stddraw.setPenColor(Color(0, 0, 0))
      stddraw.text(img_center_x + 4.75, 11, "<-")
      # Back Button
      b_button_w, b_button_h = 2, 2
      b_button_blc_x, b_button_blc_y = img_center_x - b_button_w / 2, 1
      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(b_button_blc_x, b_button_blc_y, b_button_w, b_button_h)
      stddraw.setPenColor(text_color)
      stddraw.text(img_center_x, 2, "Start")
      # Music On-Off Button
      if (player.getMusicCondition()):
         stddraw.setPenColor(Color(9, 255, 0))
      else:
         stddraw.setPenColor(Color(255, 0, 42))
      stddraw.filledRectangle(img_center_x + 6, 12.7, 0.5, 0.5)
      # Music Volume
      stddraw.setPenColor(button_color)
      stddraw.text(img_center_x + 6.2, 15, str(player.getVolume()))
      # check if the mouse has been left-clicked on the any button
      if stddraw.mousePressed():
         # get the coordinates of the most recent location at which the mouse
         # has been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the music volume increase button
         if mouse_x >= img_center_x + 7 and mouse_x <= img_center_x + 7 + 2:
            if mouse_y >= 14 and mouse_y <= 15.3:
               player.increaseVolume(5)
         # check if these coordinates are inside the music volume decrease button
         if mouse_x >= img_center_x + 5 and mouse_x <= img_center_x + 6:
            if mouse_y >= 14 and mouse_y <= 15.3:
               player.decreaseVolume(5)
         # check if these coordinates are inside the difficulty right button
         if mouse_x >= img_center_x + 7.5 and mouse_x <= img_center_x + 8:
            if mouse_y >= 10 and mouse_y <= 11:
               if (player.getDiff() <= 1):
                  player.setDiff(player.getDiff() + 1)
         # check if these coordinates are inside the difficulty left button
         if mouse_x >= img_center_x + 4.5 and mouse_x <= img_center_x + 5:
            if mouse_y >= 10 and mouse_y <= 11:
               if (player.getDiff() >= 1):
                  player.setDiff(player.getDiff() - 1)
         # check if these coordinates are inside the music on-off button
         if mouse_x >= img_center_x + 6 and mouse_x <= img_center_x + 6 + 2:
            if mouse_y >= 12 and mouse_y <= 14:
               if (player.getMusicCondition()):
                  player.turnMusicOff()
               else:
                  player.turnMusicOn()
         # check if these coordinates are inside the back button
         if mouse_x >= b_button_blc_x and mouse_x <= b_button_blc_x + b_button_w:
            if mouse_y >= b_button_blc_y and mouse_y <= b_button_blc_y + b_button_h:
               break
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
   player.updateOnClose()

# Checks each row if they are completely filled with tiles and returns each row in an array
# If a row is completely filled, it takes True value; otherwise, False
def is_full(grid_h, grid_w, grid):
   # Creates an array with all False values, with size equal to the number of rows in the game grid
   row_count = [False for _ in range(grid_h)]
   # If a row is full, this score variable keeps the total score which will come from this full row
   score = 0
   for h in range(grid_h):
      # Keeps track of the total number of tiles inside the same row; if counter == grid_w, the row is full
      counter = 0
      for w in range(grid_w):
         if grid.is_occupied(h, w):
            counter += 1
         # If the row is full, calculates the total score in this row
         if counter == grid_w:
            score = sum(grid.tile_matrix[h][a].number for a in range(grid_w))
            row_count[h] = True
   # Updates the total score
   grid.score += score
   return row_count

# Searches and finds tiles which do not connect to others
def search_free_tiles(grid_h, grid_w, labels, free_tiles):
   counter = 0
   ready_labels = []
   for x in range(grid_h):
      for y in range(grid_w):
         if labels[x, y] != 1 and labels[x, y] != 0:
            if x == 0:
               ready_labels.append(labels[x, y])
               if not ready_labels.count(labels[x, y]):
                  free_tiles[x][y] = True
                  counter += 1
   return free_tiles, counter

def apply_merge(grid):
      height = len(grid.tile_matrix)
      width = len(grid.tile_matrix[0])
      merged = False

      for y  in range(width):
          x = 0
          while x < height -1 :
             if grid.tile_matrix[x][y] != None and grid.tile_matrix[x + 1][y] != None:
                if grid.tile_matrix[x][y].number == grid.tile_matrix[x + 1][y].number:
                   # Merge the tiles
                   grid.tile_matrix[x][y].number += grid.tile_matrix[x + 1][y].number
                   grid.score += grid.tile_matrix[x][y].number
                   grid.tile_matrix[x + 1][y].number = None
                   x += 1
                   merged  = True
             x += 1
      return merged



# start() function is specified as the entry point (main function) from which
# the program starts execution

if __name__ == '__main__':
   start()
