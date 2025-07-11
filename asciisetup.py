import gamesetup as gs
import pygame

class AsciiWindow(pygame.Surface):
    '''AsciiWindow inherits from Surface
    creates a surface that's configured for ascii art games'''

    def __init__(self, game, size = (500, 500), fontSize = 12, fillColor = 0):
        '''AsciiWindow(Game, (int, int), int) -> AsciiWindow
        sets up the ascii window'''
        pygame.Surface.__init__(self, size)

        # window attributes
        self.baseBg = ""
        self.currentBg = ""
        self.bgColor = (0, 0, 0)
        self.textColor = (255, 255, 255)
        self.sprites = []
        self.font = pygame.font.SysFont("courier", fontSize)
        self.fontSize = fontSize
        self.colorMap = {}
        self.scheduledDrawings = []
        self.permanentInk = {}
        self.buttons = {}
        
        # calculate consistent character dimensions
        self.charSpacing = self.fontSize / 3
        self.charWidth, self.charHeight = self.calculate_char_dimensions()

    def calculate_char_dimensions(self):
        '''AsciiWindow.calculate_char_dimensions() -> (int, int)
        calculates consistent character width and height for square characters'''
        # test with a common character to get dimensions
        testChar = self.font.render(".", True, (255, 255, 255))
        charWidth = testChar.get_width()
        charHeight = testChar.get_height()
        
        # ensure square characters by using the smaller dimension
        # this keeps ASCII art proportional
        squareSize = min(charWidth, charHeight)
        return squareSize + self.charSpacing, squareSize + self.charSpacing

    def set_base_bg(self, textColor, bgColor, text, isTextFile = False):
        '''AsciiWindow.set_base_bg((int, int, int), (int, int, int), str, bool) -> None
        sets the base background color and ascii.
        If isTextFile is set to true, it will open a file and get the ascii there'''
        self.bgColor = bgColor
        self.textColor = textColor

        # get ascii
        if isTextFile:
            try:
                with open(text, 'r') as file:
                    self.baseBg = file.read()
            except FileNotFoundError:
                self.baseBg = text
        else:
            self.baseBg = text

    def get_bg(self, isBase = False):
        '''AsciiWindow.get_bg(bool) -> str
        returns the base background if isBase = True
        otherwise, returns updated background'''
        if isBase:
            return self.baseBg
        return self.currentBg

    def draw(self, newAsciiArt, position, color = None):
        '''AsciiWIndow.draw(str, (int, int), str) -> None
        adds the ascii for a sprite to the background
        preserves the base background'''
        self.scheduledDrawings.append([newAsciiArt, position, color])

    def write(self, text, position, color = None, leftAligned = True):
        '''AsciiWindow.write(str, (int, int), str, bool) -> None
        writes text at location using color
        set leftAligned to False to make the text right aligned'''
        row = position[0]
        col = position[1] if leftAligned else position[1] - len(text)
        self.draw(text, (row, col), color)

    def permanent_ink(self, ref, text, position, color = None, leftAligned = True):
        '''AsciiWindow.permanent_ink(str str, (int, int), str, bool) -> None
        writes text at location using color
        set leftAligned to False to make the text right aligned
        text will not going away when written
        can be deleted using the ref'''
        row = position[0]
        col = position[1] if leftAligned else position[1] - len(text)
        self.permanentInk[ref] = [text, (row, col), color]

    def delete_permanent_ink(self, ref):
        '''AsciiWindow.delete_permanent_ink(str) -> None
        deletes a permanent ink text using its ref'''
        if ref in self.permanentInk:
            self.permanentInk.pop(ref)

    def get_sprites(self):
        '''AsciiWindow.get_sprites() -> list
        returns the list of sprites'''
        return self.sprites

    def add_sprite(self, sprite):
        '''AsciiWindow.add_sprite() -> None
        adds a sprite to the window'''
        if not sprite in self.sprites:
            self.sprites.append(sprite)

    def _insert_ascii_in_bg(self, bg, art, position, color = None):
        '''AsciiWindow._insert_ascii_in_bg(str, str, (int, int)) -> str
        inserts the ascii art at the row, col in the background'''
        bgLines = bg.split("\n")
        artLines = art.split("\n")
        row, col = position
        
        for index in range(len(artLines)):
            targetRow = row + index
            
            # skip if we're trying to insert beyond the background
            if targetRow >= len(bgLines):
                break
                
            # get the current background line
            bgLine = bgLines[targetRow]
            
            # if the insertion point is beyond the current line length, pad with spaces
            if col > len(bgLine):
                bgLine = bgLine.ljust(col)
            
            # replace characters in the background with art characters
            bgLineList = list(bgLine)
            artLine = artLines[index]
            
            for i in range(len(artLine)):
                targetCol = col + i
                if artLine[i] != ' ':
                    if targetCol < len(bgLineList):
                        bgLineList[targetCol] = artLine[i]
                    else:
                        # extend the line if needed for non-space characters
                        bgLineList.extend([' '] * (targetCol - len(bgLineList) + 1))
                        bgLineList[targetCol] = artLine[i]

                    # add color at location if needed
                    if color != None:
                        self.colorMap[(targetRow, targetCol)] = color
        
            bgLines[targetRow] = ''.join(bgLineList)
    
        return "\n".join(bgLines)

    def is_touching_sprite(self, ref, coord):
        '''AsciiWindow.is_touching_sprite(str, (float, float)) -> bool
        returns if the x,y coordinate overlaps with any non space characters in the sprite'''
        # find the sprite with the given ref
        targetSprite = None
        for sprite in self.sprites:
            if hasattr(sprite, 'ref') and sprite.ref == ref:
                targetSprite = sprite
                break
        
        if targetSprite == None:
            return False
            
        # get the current frame of the sprite
        currentFrame = targetSprite.get_current_frame()
        if not currentFrame:
            return False
            
        # convert pixel coordinates to character coordinates
        charRow = int(coord[1] // self.charHeight)
        charCol = int(coord[0] // self.charWidth)
        
        # get sprite position
        spriteRow, spriteCol = targetSprite.pos()
        
        # check if coordinate is within sprite bounds
        frameLines = currentFrame.split('\n')
        for i, line in enumerate(frameLines):
            for j, char in enumerate(line):
                if char != ' ':
                    if charRow == spriteRow + i and charCol == spriteCol + j:
                        return True
        return False

    def add_button(self, ref, text, position, action, color = (200, 200, 200), hoverColor = (255, 255, 0)):
        '''AsciiWindow.add_button(str, str, (int, int), function, (int, int, int), (int, int, int)) -> None
        adds a button to the window
        color: default button color (default: light gray)
        hoverColor: color when mouse hovers over button (default: yellow)'''
        self.buttons[ref] = {
            'text': text,
            'position': position,
            'action': action,
            'isVisible': True,
            'isDisabled': False,
            'isHovered': False,
            'color': color,
            'hoverColor': hoverColor
        }

    def update_button(self, ref, text = None, position = None, action = None, isVisible = None, isDisabled = None, color = None, hoverColor = None):
        '''AsciiWindow.update_button(str, str, (int, int), function, bool, bool, (int, int, int), (int, int, int)) -> None
        updates a current button using the ref
        color: new button color
        hoverColor: new hover color'''
        if ref not in self.buttons:
            return
            
        button = self.buttons[ref]
        if text != None:
            button['text'] = text
        if position != None:
            button['position'] = position
        if action != None:
            button['action'] = action
        if isVisible != None:
            button['isVisible'] = isVisible
        if isDisabled != None:
            button['isDisabled'] = isDisabled
        if color != None:
            button['color'] = color
        if hoverColor != None:
            button['hoverColor'] = hoverColor

    def handle_mouse_click(self, mousePos):
        '''AsciiWindow.handle_mouse_click((int, int)) -> None
        handles mouse clicks for buttons'''
        charRow = int(mousePos[1] // self.charHeight)
        charCol = int(mousePos[0] // self.charWidth)
        
        for ref, button in self.buttons.items():
            if not button['isVisible'] or button['isDisabled']:
                continue
                
            buttonRow, buttonCol = button['position']
            buttonText = button['text']
            
            # check if click is within button bounds
            if (charRow == buttonRow and 
                buttonCol <= charCol < buttonCol + len(buttonText)):
                if button['action']:
                    button['action']()
                break

    def handle_mouse_move(self, mousePos):
        '''AsciiWindow.handle_mouse_move((int, int)) -> None
        handles mouse movement for button hover'''
        charRow = int(mousePos[1] // self.charHeight)
        charCol = int(mousePos[0] // self.charWidth)
        
        for ref, button in self.buttons.items():
            if not button['isVisible'] or button['isDisabled']:
                button['isHovered'] = False
                continue
                
            buttonRow, buttonCol = button['position']
            buttonText = button['text']
            
            # check if mouse is over button
            button['isHovered'] = (charRow == buttonRow and 
                                 buttonCol <= charCol < buttonCol + len(buttonText))

    def update(self):
        '''AsciiWindow.update() -> None
        updates the ascii window'''
        # update the background color
        self.fill(self.bgColor)

        # start with background text
        self.colorMap.clear()
        self.currentBg = self.baseBg
        
        # add all sprites to the background
        for sprite in self.sprites:
            sprite.update()

        # draw all buttons
        for ref, button in self.buttons.items():
            if button['isVisible']:
                color = None
                if button['isDisabled']:
                    color = (100, 100, 100)
                elif button['isHovered']:
                    color = button['hoverColor']
                else:
                    color = button['color']
                    
                self.draw(button['text'], button['position'], color)

        # now actually draw everything
        for ink in self.permanentInk:
            text = self.permanentInk[ink]
            self.currentBg = self._insert_ascii_in_bg(self.currentBg, text[0], text[1], text[2])
        for drawing in self.scheduledDrawings:
            self.currentBg = self._insert_ascii_in_bg(self.currentBg, drawing[0], drawing[1], drawing[2])
        self.scheduledDrawings.clear()
        
        # render the text with consistent character spacing
        if self.currentBg:
            lines = self.currentBg.split('\n')
            yOffset = 0
            for i in range(len(lines)):
                line = lines[i]
                xOffset = 0
                for j in range(len(line)):
                    char = line[j]

                    # render the character
                    if char != ' ':
                        color = self.colorMap[(i,j)] if (i,j) in self.colorMap else self.textColor
                        charSurface = self.font.render(char, True, color)
                        
                        # center the character in its allocated space
                        charX = xOffset + (self.charWidth - charSurface.get_width()) // 2
                        charY = yOffset + (self.charHeight - charSurface.get_height()) // 2
                        self.blit(charSurface, (charX, charY))
                    xOffset += self.charWidth
                yOffset += self.charHeight

class AsciiSprite:
    '''creates a sprite-like object that you can display using AsciiWindow'''

    def __init__(self, window, position, ref = None):
        '''AsciiSprite(AsciiWindow, (int, int), str) -> AsciiSprite
        sets up the ascii sprite
        window: the screen it will be rendered on
        position: is the row and col that it will be rendered
        ref: optional reference id for sprite identification'''
        self.window = window
        self.position = position
        self.ref = ref
        self.window.add_sprite(self)

        # frame bundle setup
        self.frameBundles = {}
        self.currentAscii = ""
        self.currentRef = None
        
    def get_current_frame(self):
        '''AsciiSprite.get_current_frame() -> str
        returns the current ascii art frame for the sprite'''
        if self.currentRef:
            frames, delay, index, clock, color = self.frameBundles[self.currentRef]
            return frames[index]
        return ""

    def add_frame_bundle(self, ref, frames, delay = None, color = None):
        '''add_frame_bundle(str, str[], int, str) -> None
        adds a new frame bundle to the sprite
        ref: the reference id for the bundle
        frames: list of ascii art frames
        deley: the delay between a frame switch (set to None if it doesn't change)

        a frame bundle is a series of ascii frames that can be animated
        each bundle consists of the list of frames (strings), the
        delay (in ms) between frames, and the current frame index
        includes a gamesetup clock to track when to switch
        includes the color of the frame
        they also have a reference id (ref) that's used to switch between them'''
        # build the bundle
        if delay != None:
            clock = gs.Clock(delay / 1000)
        else:
            clock = None
        self.frameBundles[ref] = [frames, delay, 0, clock, color]

        # switch to this bundle if currentRef is None
        if not self.currentRef:
            self.switch_frame_bundle(ref)

    def switch_frame_bundle(self, ref):
        '''AsciiSprite.switch_frame_bundle(str) -> None
        switches to the frame bundle using the reference id (ref)'''
        clock = self.frameBundles[ref][3]
        if clock != None:
            clock.reset()
            clock.start()
        self.currentRef = ref

    def pos(self, position = None):
        '''AsciiSprite.pos((int, int)) -> (int, int)
        if position is specified, sets the row and col
        otherwise, returns the position'''
        if position == None:
            return self.position
        self.position = position
        
    def update(self):
        '''AsciiSprite.update() -> None
        updates the sprite, include the current frame bundle'''
        if not self.currentRef:
            return

        # get the frame bundle info
        bundle = self.frameBundles[self.currentRef]
        frames, delay, currentFrameIndex, clock, color = bundle
        currentFrame = frames[currentFrameIndex]

        # update the bundle
        if delay != None and clock != None and clock.get_time() >= clock.get_max():
            currentFrameIndex = (currentFrameIndex + 1) % len(frames)
            bundle[2] = currentFrameIndex
            currentFrame = frames[currentFrameIndex]
            clock.reset()
            clock.start()

        # display the frame
        self.window.draw(currentFrame, self.pos(), color)

# Enhanced Test Game with Button Example
class TestGame(gs.Game):
    def __init__(self):
        gs.Game.__init__(self, (800, 600), "ASCII Art Game")
        self.asciiWindow = AsciiWindow(self, (800, 600), 20)
        self.asciiWindow.set_base_bg((255, 255, 255), (0, 0, 0), ("." * 40 + "\n") * 30, False)
        
        # create a test sprite with square ASCII art and ref
        self.testSprite = AsciiSprite(self.asciiWindow, (5, 10), "player")
        self.testSprite.add_frame_bundle("idle", ["\\ /\n-|-\n/ \\"], 500, (0, 255, 0))
        
        # add some buttons with custom colors
        self.asciiWindow.add_button("start", "Start Game", (2, 2), self.start_game, (0, 255, 0), (0, 200, 0))
        self.asciiWindow.add_button("quit", "Quit", (3, 2), self.quit_game, (255, 0, 0), (200, 0, 0))
        self.asciiWindow.add_button("move", "Move Player", (4, 2), self.move_player)  # uses defaults
        
        # bind mouse events
        self.bind(pygame.MOUSEBUTTONDOWN, self.mouse_click)
        self.bind(pygame.MOUSEMOTION, self.mouse_move)
        
    def start_game(self):
        print("Game Started!")
        self.asciiWindow.update_button("start", isDisabled = True)
        
    def quit_game(self):
        print("Quitting...")
        self.close()
        
    def move_player(self):
        import random
        newRow = random.randint(5, 25)
        newCol = random.randint(5, 35)
        self.testSprite.pos((newRow, newCol))
        
    def mouse_click(self, event):
        self.asciiWindow.handle_mouse_click(event.pos)
        
    def mouse_move(self, event):
        self.asciiWindow.handle_mouse_move(event.pos)
        
        # test sprite touching
        if self.asciiWindow.is_touching_sprite("player", event.pos):
            self.asciiWindow.permanent_ink("message", "Touching Player!", (1, 1), (255, 0, 0))
        else:
            self.asciiWindow.delete_permanent_ink("message")
        
    def update(self):
        self.asciiWindow.update()
        self.blit(self.asciiWindow, (0, 0))

if __name__ == "__main__":
    pygame.init()
    game = TestGame()
    game.mainloop()
