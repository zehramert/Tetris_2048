# TETRIS_2048 GAME

This project is a combination of 2 games: Tetris and 2048. By controlling tetrominoes, which are various shapes composed of four blocks each, as they fall onto a grid. Every block is identified by a number that denotes its value. At first, the tetrominoes are just randomly assigned with 2 or 4 numbers on them. Blocks that have the same number merged together earn points. Points are awarded based on the value of the combined block, which doubles when two identical vertical blocks come into contact with each other. By carefully combining blocks, the goal is to get to a block that has the number 2048. To clear full rows, you also try to fill them with blocks. You gain points for clearing rows as well, which are determined by adding up the block values in the row

### Components:
Game Grid: Manages the layout where tetrominoes are placed and manipulated. Includes functions to check full rows, merging operations and update colors based on numeric value.
Game Mechanics: Handles up-down-left-right and rotate moves on tetromino within the grid. Includes gravity-like mechanics where pieces fall and lock based on the game's physics rules and function for hard drop.
User-Interface: Displays the game state visually and provides interactive menus for pause, game over, and settings, allowing players to make selections
Settings and Customizations: Allows players to adjust volume, select music on/off, and change difficulty levels and saves high scores
Event Handling: Processes input from the mouse and keyboard to control game elements and navigate menus.

### Usage:
* Use arrow keys to control falling tetrominoes.
* Use up arrow key for rotate tetrominoes.
* Use space for hard drop.


<img src="https://github.com/zehramert/Tetris_2048/blob/main/Screenshot%202024-05-01%20at%2021.46.16.png" alt="" width="320">  <img src="https://github.com/zehramert/Tetris_2048/blob/main/Screenshot%202024-05-01%20at%2021.46.26.png" alt="" width="320">

<img src="https://github.com/zehramert/Tetris_2048/blob/main/Screenshot%202024-05-01%20at%2021.46.49.png" alt="" width="640">

<img src="https://github.com/zehramert/Tetris_2048/blob/main/Screenshot%202024-05-01%20at%2021.47.29.png" alt="" width="320"> <img src="https://github.com/zehramert/Tetris_2048/blob/main/Screenshot%202024-05-01%20at%2021.47.13.png" alt="" width="320">








