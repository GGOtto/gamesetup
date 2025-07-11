import gamesetup as gs
from asciisetup import *
import pygame
import random

class SnakeGame(gs.Game):
    '''simple snake game'''
    
    def __init__(self):
        size = (597, 400)
        gs.Game.__init__(self, size, "Snake Game")
        
        # game board
        self.boardWidth = 39
        self.boardHeight = 26
        
        # snake
        self.snake = [(10, 15), (10, 14), (10, 13)]
        self.direction = (0, 1)
        self.newDirections = []
        
        # game state
        self.gameOver = False
        self.score = 0
        
        # timer
        self.moveTimer = gs.Clock(0.2)
        self.moveTimer.start()
        
        # ascii window
        self.asciiWindow = AsciiWindow(self, size, 16)
        self.create_board()

        # food
        self.food = AsciiSprite(self.asciiWindow, (7, 7))
        self.food.add_frame_bundle("glow", [".", "o", "O", "o"], 200, "red")
        self.spawn_food()
        
        # controls
        self.bind(pygame.KEYDOWN, self.handle_key)
        self.asciiWindow.add_button("restart", "RESTART?", (self.boardHeight - 2, 5), self.__init__, "lime", "dark green")
        self.asciiWindow.update_button("restart", isVisible = False)
        self.bind(pygame.MOUSEBUTTONDOWN, self.mouse_click)
        self.bind(pygame.MOUSEMOTION, self.mouse_move)
        
    def create_board(self):
        '''creates the game board'''
        self.asciiWindow.set_base_bg((50, 50, 50), (0, 0, 0), ("." * self.boardWidth + "\n") * self.boardHeight)

        # now make the edges
        board = []
        for row in range(self.boardHeight):
            if row < 3 or row > self.boardHeight - 4:
                board.append("#" * self.boardWidth)
            else:
                board.append("#" * 3+ " " * (self.boardWidth - 6) + "#" * 3)
        
        boardText = "\n".join(board)
        self.asciiWindow.permanent_ink("edges", boardText, (0, 0), (150, 150, 150))

    def verify_new_direction(self, newDir):
        '''checks to see if the snake can move in dir, which is "up", "down", "left", or "right"'''
        head = self.snake[0]
        neck = self.snake[1]
        oldDir = head[0] - neck[0], head[1] - neck[1]

        return (newDir == "up" and oldDir != (1, 0)) or \
               (newDir == "down" and oldDir != (-1, 0)) or \
               (newDir == "left" and oldDir != (0, 1)) or \
               (newDir == "right" and oldDir != (0, -1))

    def last_direction(self):
        '''gets the last direction, including current dir and last in scheduled moves'''
        if len(self.newDirections):
            return self.newDirections[-1]
        return self.direction
        
    def handle_key(self, event):
        '''handles key input'''
        if self.gameOver:
            return
            
        if event.key == pygame.K_UP and self.last_direction() != (1, 0):
            self.newDirections.append((-1, 0))
        elif event.key == pygame.K_DOWN and self.last_direction() != (-1, 0):
            self.newDirections.append((1, 0))
        elif event.key == pygame.K_LEFT and self.last_direction() != (0, 1):
            self.newDirections.append((0, -1))
        elif event.key == pygame.K_RIGHT and self.last_direction() != (0, -1):
            self.newDirections.append((0, 1))
            
    def move_snake(self):
        '''moves the snake'''
        # turn the snake
        if len(self.newDirections) > 0:
            self.direction = self.newDirections.pop(0)
            
        head = self.snake[0]
        newHead = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # check wall collision
        if (newHead[0] <= 2 or newHead[0] >= self.boardHeight - 3 or 
            newHead[1] <= 2 or newHead[1] >= self.boardWidth - 3):
            self.asciiWindow.update_button("restart", isVisible = True)
            self.gameOver = True
            return
            
        # check self collision
        if newHead in self.snake:
            self.asciiWindow.update_button("restart", isVisible = True)
            self.gameOver = True
            return
            
        # add new head
        self.snake.insert(0, newHead)
        
        # check food
        if newHead == self.food.pos():
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()
            
    def spawn_food(self):
        '''spawns food at random location'''
        while True:
            row = random.randint(4, self.boardHeight - 5)
            col = random.randint(4, self.boardWidth - 5)
            if (row, col) not in self.snake:
                self.food.pos((row, col))
                break

    def mouse_click(self, event):
        '''runs on mouse click'''
        self.asciiWindow.handle_mouse_click(event.pos)
        
    def mouse_move(self, event):
        '''runs on move movement'''
        self.asciiWindow.handle_mouse_move(event.pos)
                
    def update(self):
        '''main game update'''
        if not self.gameOver:
            # move snake
            if self.moveTimer.get_time() >= self.moveTimer.get_max():
                self.move_snake()
                self.moveTimer.reset()
                self.moveTimer.start()
        
        # update display
        self.asciiWindow.update()
        
        # draw snake
        for i, (row, col) in enumerate(self.snake):
            char = "O" if i == 0 else "o"
            color = (0, 255, 0) if i == 0 else (0, 200, 0)
            self.asciiWindow.draw(char, (row, col), color)
        
        # draw score
        self.asciiWindow.write(f"Score: {self.score}", (1, self.boardWidth - 5), "lime", False)
        if self.gameOver:
            self.asciiWindow.write("GAME OVER", (1, 5), "lime")
            
        # draw to screen
        self.blit(self.asciiWindow, (0, 0))

if __name__ == "__main__":
    pygame.init()
    game = SnakeGame()
    game.mainloop()
