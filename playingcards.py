# Name: Playing Cards
# Author: Oliver White
# Date: 8/20/24
# Version 1.0.0
#
# Used with the pygame module
# Also requires gamesetup 1.9.5

import pygame, time, random, math
import gamesetup as gs

global GAME_VERSION
GAME_VERSION = "1.0.0"

def _draw_diamond_for_back_design(surface, color, x, y, width, height):
    '''_draw_diamond_for_back_design(
        pygame.Surface, (r,g,b), x, y,
        width, height
    ) -> None
    draws a diamond shape on the surface in the specified color
    used for the back design of the cards'''
    # vertices for the diamond
    halfWidth = math.floor(width / 2)
    halfHeight = math.floor(height / 2)

    verticesInner = [
        (x - halfWidth, y),
        (x, y - halfHeight),
        (x + halfWidth, y),
        (x, y + halfHeight - 1)
    ]
    
    verticesOuter = [
        (x - halfWidth, y),
        (x, y - halfHeight),
        (x + halfWidth, y),
        (x, y + halfHeight),
    ]

    # draw diamond
    pygame.draw.polygon(surface, color, verticesInner)
    pygame.draw.aalines(surface, color, True, verticesOuter)

def _draw_card_numbered_suit_layout(surface, face, suit, flippedSuit, width, height):
    '''_draw.card_numbered_suit_layout(pygame.Surface, str, pygame.Surface, pygame.Surface, int, int) -> None
    draws the card suit layout for aces and numbered cards'''

    # position for faces 2-10
    suitPositions = (
        (   # 2s
            (suit, (width / 2, height / 5)),
            (flippedSuit, (width / 2, 4 * height / 5))
        ),
        (   # 3s
            (suit, (width / 2, height / 5)),
            (suit, (width / 2, height / 2)),
            (flippedSuit, (width / 2, 4 * height / 5))
        ),
        (   # 4s
            (suit, (width / 3.5, height / 5)),
            (suit, (2.5 * width / 3.5, height / 5)),
            (flippedSuit, (width / 3.5, 4 * height / 5)),
            (flippedSuit, (2.5 * width / 3.5, 4 * height / 5))
        ),
        (   # 5s
            (suit, (width / 3.5, height / 5)),
            (suit, (2.5 * width / 3.5, height / 5)),
            (suit, (width / 2, height / 2)),
            (flippedSuit, (width / 3.5, 4 * height / 5)),
            (flippedSuit, (2.5 * width / 3.5, 4 * height / 5)),
        ),
        (   # 6s
            (suit, (width / 3.5, height / 5)),
            (suit, (2.5 * width / 3.5, height / 5)),
            (suit, (width / 3.5, height / 2)),
            (suit, (2.5 * width / 3.5, height / 2)),
            (flippedSuit, (width / 3.5, 4 * height / 5)),
            (flippedSuit, (2.5 * width / 3.5, 4 * height / 5)),
        ),
        (   # 7s
            (suit, (width / 3.5, height / 5)),
            (suit, (2.5 * width / 3.5, height / 5)),
            (suit, (width / 2, 7 * height / 20)),
            (suit, (width / 3.5, height / 2)),
            (suit, (2.5 * width / 3.5, height / 2)),
            (flippedSuit, (width / 3.5, 4 * height / 5)),
            (flippedSuit, (2.5 * width / 3.5, 4 * height / 5)),
        ),
        (   # 8s
            (suit, (width / 3.5, height / 5)),
            (suit, (2.5 * width / 3.5, height / 5)),
            (suit, (width / 2, 7 * height / 20)),
            (suit, (width / 3.5, height / 2)),
            (suit, (2.5 * width / 3.5, height / 2)),
            (flippedSuit, (width / 2, 27 * height / 40)),
            (flippedSuit, (width / 3.5, 4 * height / 5)),
            (flippedSuit, (2.5 * width / 3.5, 4 * height / 5)),
        ),
        (   # 9s
            (suit, (width / 3.5, height / 5)),
            (suit, (2.5 * width / 3.5, height / 5)),
            (suit, (width / 3.5, 31 * height / 80)),
            (suit, (2.5 * width / 3.5, 31 * height / 80)),
            (suit, (width / 2, height / 2)),
            (flippedSuit, (width / 3.5, 49 * height / 80)),
            (flippedSuit, (2.5 * width / 3.5, 49 * height / 80)),
            (flippedSuit, (width / 3.5, 4 * height / 5)),
            (flippedSuit, (2.5 * width / 3.5, 4 * height / 5)),
        ),
        (   # 10s
            (suit, (width / 3.5, height / 5)),
            (suit, (2.5 * width / 3.5, height / 5)),
            (suit, (width / 2, 3 * height / 10)),
            (suit, (width / 3.5, 31 * height / 80)),
            (suit, (2.5 * width / 3.5, 31 * height / 80)),
            (flippedSuit, (width / 3.5, 49 * height / 80)),
            (flippedSuit, (2.5 * width / 3.5, 49 * height / 80)),
            (flippedSuit, (width / 2, 7 * height / 10)),
            (flippedSuit, (width / 3.5, 4 * height / 5)),
            (flippedSuit, (2.5 * width / 3.5, 4 * height / 5)),
        ),
    )

    # draw the card
    if face.isalpha():
        gs.blit(surface, suit, (width / 2, height / 2), True, True)
    else:
        for suitPos in suitPositions[int(face) - 2]:
            gs.blit(surface, suitPos[0], suitPos[1], True, True)
    
    
class Card(gs.Widget):
    '''represents a single playing card'''

    def __init__(self, game, card = ("10", "heart", "red"), size = "medium",
            backColor = (21, 60, 129), outlineColor = (50,50,50), outlineWidth = 2):
        '''Card(gs.Game, (face, suit, color), size, backColor, outlineColor, outlineWidth) -> Card
        sets up a card to use on a gamesetup Game object
        game: the game to draw the card on
        suit: "hearts", "diamonds", "spades", "clubs", or "JOKER"
        number: A, 1-10, J, Q, K, or JOKER
        color: any color to display the cards
        size: either "tiny", "small", "medium", or "large"'''

        # info for colors, faces, and suits
        self.faces = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "JOKER", "EMPTY"]
        self.suits = {"spade": "♠", "heart": "♥", "club": "♣", "diamond": "♦", "JOKER": "♪"}

        # check to see if a card is valid
        if not card[0] in self.faces:
            raise gs.GameSetupError(f"Face {card[0]} not valid for playing card")
        elif not card[1] in self.suits:
            raise gs.GameSetupError(f"Suit {card[1]} not valid for playing card")
        
        # set up the card sizes        
        self.size = size
        self.sizes = get_sizes(outlineWidth)
        
        # set up the gamesetup widget
        gs.Widget.__init__(self, game, (0, 0, self.sizes[size][0], self.sizes[size][1]), True)
        
        # card attributes
        self.game = game
        self.face = card[0]
        self.suit = card[1]
        self.color = card[2]
        self.backColor = backColor
        self.size = size
        self.currentSide = "back"
        self.sides = {}
        self.outlineWidth = outlineWidth
        self.outlineColor = outlineColor
        self.shakeClock = gs.Clock()
        self.shakeViolence = 1
        self.position = 0,0
        self.isMoving = False
        self.moveClock = gs.Clock()
        self.rotation = 0
        self.font = "segoeprint"

        # font info for different sizes
        self.fontSizes = {
            "tiny": 21, "small": 18, "medium":  18, "large": 22
        }
        self.jokerFontSize = {
            "tiny": 11, "small": 16, "medium": 24, "large": 36
        }
        self.faceFontSizes = {
            "tiny": 0, "small": 0, "medium": 50, "large": 85
        }
        self.centerFontSizes = {
            "tiny": 0, "small": 0, "medium": 40, "large": 50
        }
        
        self.render_sides()

    def __eq__(self, secondCard):
        '''Card.__eq__(Card) -> bool
        returns if the given card's id matches this card'''
        return self.get_id() == secondCard.get_id()

    def __str__(self):
        '''str(Card) -> str
        return a string version of the card'''
        return f"{self.color} {self.face} of {self.suit}s"

    def get_width(self):
        '''Card.get_width() -> int
        returns the width of the card'''
        return self.sides[f"display-{self.currentSide}"].get_width()

    def get_height(self):
        '''Card.get_height() -> int
        returns the height of the card'''
        return self.sides[f"display-{self.currentSide}"].get_height()

    def get_rect(self):
        '''Card.get_rect() -> (x,y,w,h)
        returns the card's current rectangle'''
        return gs.Widget.get_rect(self)[0], gs.Widget.get_rect(self)[1], \
            self.get_width(), self.get_height()

    def render_sides(self, redraw=True):
        '''Card.render_sides(redraw=True) -> None
        renders the sides of the cards
        if redraw is False, only rotates the cards'''
        if redraw:
            self.sides["face"] = self.build_face()
            self.sides["back"] = self.build_back()

        # now rotate the cards
        if self.rotation != 0:
            self.sides["display-face"] = pygame.transform.rotozoom(
                self.sides["face"], self.rotation, 1)
            self.sides["display-back"] = pygame.transform.rotozoom(
                self.sides["back"], self.rotation, 1)
        else:
            self.sides["display-face"] = self.sides["face"]
            self.sides["display-back"] = self.sides["back"]

        self.set_rect(self.get_rect())        
        
    def get_suit(self):
        '''Card.get_suit() -> str
        returns the suit of the card'''
        return self.suit

    def set_suit(self, suit):
        '''Card.set_suit(str) -> None
        sets the suit of the card'''
        self.suit = suit
        self.render_sides()

    def get_color(self):
        '''Card.get_color() -> color
        returns the color of the card'''
        return self.color

    def set_color(self, color):
        '''Card.set_color(str) -> None
        sets the suit of the card'''
        self.color = color
        self.render_sides()

    def get_face(self):
        '''Card.get_face() -> str
        returns the face of the card'''
        return self.face

    def set_face(self, face):
        '''Card.set_face(str) -> None
        sets the face of the card'''
        self.suit = face
        self.render_sides()

    def get_back_color(self):
        '''Card.get_back_color() -> color
        returns the color of the back of the card'''
        return self.backColor

    def set_back_color(self, color):
        '''Card.set_back_color(str) -> None
        sets the color of the back of the card'''
        self.backColor = color
        self.render_sides()

    def get_size(self):
        '''Card.get_size() -> str
        returns the size of the card'''
        return self.size

    def set_size(self, size):
        '''Card.set_size(str) -> None
        sets the size of the card'''
        self.size = size
        self.render_sides()

    def get_outline_color(self):
        '''Card.get_outline_color() -> str
        returns the color of the outline of the card'''
        return self.outlineColor

    def set_outline_color(self, color):
        '''Card.set_outline_color(str) -> None
        sets the color of the outline of the card'''
        self.outlineColor = color
        self.render_sides()

    def get_outline_width(self):
        '''Card.get_outline_width() -> str
        returns the width of the outline of the card'''
        return self.outlineWidth

    def set_outline_width(self, width):
        '''Card.set_outline_width(str) -> None
        sets the width of the outline of the card'''
        self.outlineWidth = width
        self.render_sides()

    def pos(self, pos = None):
        '''Card.pos(pos = None) -> (x,y)
        if pos (x,y) is given, sets the card's position
        returns the old position'''
        rect = self.get_rect()

        # set the position if given
        if pos != None:
            self.move(pos)
            self.position = pos

        return rect[0], rect[1]

    def get_current_side(self):
        '''Card.get_current_side() -> str
        returns the current side of the card (either face or back)'''
        return self.currentSide
                
    def get_sides(self):
        '''Card.get_sides() -> dict
        returns both sides of the card in a dictionary
        "face" is the key to the face
        "back" is the key to the back'''
        return self.sides

    def flip_card(self, setSide = None):
        '''Card.flip_card(setSide = None) -> "face" or "back"
        flips the card over if setSide is not given
        sets side to setSide ("face" or "back") if given
        returns the new side'''
        if setSide == None:
            if self.currentSide == "face":
                self.currentSide = "back"
            else:
                self.currentSide = "face"
        else:
            self.currentSide = setSide
        return self.currentSide

    def get_rotation(self):
        '''rotate.get_rotation() -> int
        returns the card's rotation in degrees'''
        return self.rotation

    def rotate_card(self, degrees):
        '''rotate_card(int) -> None
        rotates the card a certain amount of degrees'''
        self.rotation = degrees
        self.render_sides(False)

    def shake(self, duration, violence = 1):
        '''Card.shake(duration, violence = 1) -> None
        causes the card to perform a shake animation
        duration is in seconds
        smallest shake violence is 1'''
        self.shakeClock.set_max(duration)
        self.shakeViolence = violence
        self.shakeClock.start()

    def shake_flip(self, duration = 0.07, violence = 2):
        '''Card.shake_flip(durection = 0.07, violence = 2) -> None
        performs a quick shake before the flip for a better look'''
        self.shake(duration, violence)
        self.game.after(duration / 2 * 1000, lambda: self.flip_card())

    def _event_flip(self, event):
        '''Card._event_flip(event) -> None
        flips the cards. used for testing'''
        self.shake_flip()

    def move_to(self, dest, speed):
        '''Card.move_to(dest, speed) -> int
        moves the card to destination (dest)
        speed is in pixels/second
        returns the time it will take to move in milliseconds'''
        distance = math.sqrt((self.position[0] - dest[0])**2 + (self.position[1] - dest[1])**2)
        self.isMoving = distance > 0
        self.moveClock.set_max(distance / speed)
        self.moveDest = dest
        self.moveClock.start()
        return round(distance / speed * 1000) + 10

    def stop_moving(self):
        '''Card.stop_moving() -> None
        if the card is currently moving, stop it'''
        self.isMoving = False
        self.pos((self.get_rect()[0], self.get_rect()[1]))

    def build_face(self):
        '''Card.build_face() -> pygame.Surface
        returns a new surface with the card's face'''
        width = gs.Widget.get_rect(self)[2] - self.outlineWidth*2
        height = gs.Widget.get_rect(self)[3] - self.outlineWidth*2

        # create the pygame surface
        front = pygame.Surface((width,height))
        front.fill("white")
        fullFront = pygame.Surface((width + self.outlineWidth*2, height + self.outlineWidth*2))
        fullFront.fill(self.outlineColor)
        transparentFront = pygame.Surface(
            (width + self.outlineWidth*2, height + self.outlineWidth*2), pygame.SRCALPHA)

        # the face of the card
        if self.face != "JOKER":
            face = pygame.font.SysFont(
                self.font, self.fontSizes[self.size], True
            ).render(self.face, True, self.color)
            flippedFace = pygame.transform.flip(face, True, True)

        # the face if the card is a joker
        else:
            jokerFont = pygame.font.SysFont(
                self.font, self.jokerFontSize[self.size], True
            )

            # create each letter individually
            size = [0,0]
            letters = []
            for i in range(len(self.face)):
                newLetter = jokerFont.render(self.face[i], True, self.color)
                letters.append(newLetter)
                size[0] += newLetter.get_width() / 2 if i != len(self.face) - 1 else newLetter.get_width()
                size[1] += newLetter.get_height() * 0.6

            # add each letter to a new surface
            y = -0.2 * letters[0].get_height()
            x = 0
            face = pygame.Surface(size)
            face.fill("white")
            for letter in letters:
                face.blit(letter, (x, y))
                x += letter.get_width() / 2
                y += letter.get_height() * 0.6

            flippedFace = pygame.transform.flip(face, True, True)

        # the suit of the card        
        suit = pygame.font.SysFont(
            self.font, self.fontSizes[self.size] + 10, True
        ).render(self.suits[self.suit], True, self.color)
        flippedSuit = pygame.transform.flip(suit, True, True)

        # the center of the card
        if self.face.isalpha() and self.face != "A":
            center = pygame.font.SysFont(
                self.font, self.faceFontSizes[self.size], True
            ).render(self.face, True, self.color)
        else:
            center = pygame.font.SysFont(
                self.font, self.centerFontSizes[self.size], True
            ).render(self.suits[self.suit], True, self.color)
        flippedCenter = pygame.transform.flip(center, True, True)

        # leave the card empty
        if self.face == "EMPTY":
            pass

        # build joker card
        elif self.face == "JOKER":
            self.game.blit(face, (width / 2, height / 2), True, True, front)

        # build tiny card
        elif self.size == "tiny":
            self.game.blit(face, (width / 2, height / 2 - face.get_height() + 4),
                True, False, front)
            self.game.blit(suit, (width / 2, height / 2 - 17),
                True, False, front)

        # build small card
        elif self.size == "small":
            self.game.blit(face, (7, 0), False, False, front)
            self.game.blit(flippedFace,
                (width - flippedFace.get_width() - 7, height - flippedFace.get_height()),
                False, False, front)
            self.game.blit(suit, (width / 2, height / 2), True, True, front)

        # build medium cards
        elif self.size == "medium":
            self.game.blit(face, (7, -3), False, False, front)
            self.game.blit(flippedFace,
                (width - flippedFace.get_width() - 7, height - flippedFace.get_height() + 3),
                False, False, front)

            # deal with number cards and aces
            if self.face.isalpha() and self.face != "A":
                self.game.blit(suit, (face.get_width() / 2 + 7, face.get_height() - 23), True, False, front)
                self.game.blit(flippedSuit,
                    (width - flippedFace.get_width() / 2 - 7, height - flippedFace.get_height() - flippedSuit.get_height() + 23),
                    True, False, front)

            _draw_card_numbered_suit_layout(front, self.face, center, flippedCenter, width, height)
                
        # build large cards
        else:
            self.game.blit(face, (7, -3), False, False, front)
            self.game.blit(flippedFace,
                (width - flippedFace.get_width() - 7, height - flippedFace.get_height() + 3),
                False, False, front)
            self.game.blit(suit, (face.get_width() / 2 + (7 if self.face != "10" else 0), face.get_height() - 26), True, False, front)
            self.game.blit(flippedSuit,
                    (width - flippedFace.get_width() / 2 - (7 if self.face != "10" else 0), height - flippedFace.get_height() - flippedSuit.get_height() + 26),
                    True, False, front)

            _draw_card_numbered_suit_layout(front, self.face, center, flippedCenter, width, height)

        fullFront.blit(front, (self.outlineWidth, self.outlineWidth))
        transparentFront.blit(fullFront, (0, 0))

        return transparentFront
    
    def build_back(self):
        '''Card.build_back() -> pygame.Surface
        returns a new surface with the card's back'''
        width = gs.Widget.get_rect(self)[2] - self.outlineWidth*2
        height = gs.Widget.get_rect(self)[3] - self.outlineWidth*2

        # the size of the diamond pattern
        designWidth = 3
        designHeight = 4
        designSpacing = round(width / designWidth * 0.3)
        diamondWidth = (width - designSpacing) / designWidth - designSpacing
        diamondHeight = (height - designSpacing) / designHeight - designSpacing

        # create the pygame surface
        back = pygame.Surface((width,height))
        back.fill("white")
        fullBack = pygame.Surface((width + self.outlineWidth*2, height + self.outlineWidth*2))
        fullBack.fill(self.outlineColor)
        transparentBack = pygame.Surface(
            (width + self.outlineWidth*2, height + self.outlineWidth*2), pygame.SRCALPHA)

        # draw the outer diamond pattern
        x, y = diamondWidth / 2 + designSpacing, diamondHeight / 2 + designSpacing
        for row in range(designHeight):
            for col in range(designWidth):
                _draw_diamond_for_back_design(
                    back, self.backColor, int(x), int(y),
                    diamondWidth, diamondHeight)
                x += diamondWidth + designSpacing
            x = diamondWidth / 2 + designSpacing
            y += diamondHeight + designSpacing

        # draw the inner diamond pattern
        designWidth += 1
        designHeight += 1
        x, y = 0.5 * designSpacing, 0.5 * designSpacing
        for row in range(designHeight):
            for col in range(designWidth):
                _draw_diamond_for_back_design(
                    back, self.backColor, int(x), int(y),
                    diamondWidth, diamondHeight)
                x += diamondWidth + designSpacing
            x = 0.5 * designSpacing
            y += diamondHeight + designSpacing

        fullBack.blit(back, (self.outlineWidth, self.outlineWidth))
        transparentBack.blit(fullBack, (0, 0))

        return transparentBack

    def update(self):
        '''Card.update() -> None
        updates the card at its current position'''
        
        # shake the card
        if self.shakeClock.get_time() != self.shakeClock.get_max() and self.shakeClock.get_max() != None:
            self.move((
                self.position[0] + random.randint(-self.shakeViolence, self.shakeViolence),
                self.position[1] + random.randint(-self.shakeViolence, self.shakeViolence),
            ))
            
        # move the card
        elif self.isMoving:
            self.move((
                self.position[0] + (self.moveDest[0] - self.position[0]) * self.moveClock.get_time() / self.moveClock.get_max(),
                self.position[1] + (self.moveDest[1] - self.position[1]) * self.moveClock.get_time() / self.moveClock.get_max()
            ))
            if self.moveClock.get_time() == self.moveClock.get_max():
                self.isMoving = False
                self.pos(self.moveDest)

        # reset the card after shaking     
        else:
            self.pos(self.position)

        self.game.blit(self.sides[f"display-{self.currentSide}"], (self.get_rect()[0], self.get_rect()[1]))        

class CardDeck:
    '''represents a deck of cards'''

    def __init__(self, game, location,
        size = "medium", backColor = (21, 60, 129), outlineColor = (50,50,50), outlineWidth = 2,
        preloadDeck = None, includeJokers = True, visualStackHeight = 3, showEmptyPiles = True, preshuffle = True):
        '''CardDeck(str, (x,y), (r,g,b), (r,g,b), int, bool, bool, int, bool, bool) -> CardDeck
        buils a card deck with card's with the specified attributes
        If you want to load your own cards, set the parameter preloadDeck to your list of cards
        A single card should look this: (face, suit, color) or ("10", "heart", "red")
        Setting visualStackHeight (defaults to 3) will change the visual for the deck stack
        Setting showEmptyPiles to False (defaults to True) will make the gray squares no
            longer appear when the deck or discard pile is empty
        Setting preshuffle to False (defaults to True) will make the deck not be shuffled after loading it'''
        self.game = game
        self.deck = []
        self.discard = []
        self.deckLocation = location
        self.hasMovedDiscard = False
        self.movementSpeed = 1500
        self.eventCommand = self.process_click_of_top_card
        self.load_deck(
            size, backColor, outlineColor,
            outlineWidth, preloadDeck, includeJokers)

    def get_movement_speed(self):
        '''CardDeck.get_movement_speed() -> int
        returns the speed of the cards when going to the discard (pixels / second)'''
        return self.movementSpeed

    def set_movement_speed(self, newSpeed):
        '''CardDeck.set_movement_speed(int) -> None
        sets the speed of the cards when going to the discard (pixels / second)'''
        self.movementSpeed = newSpeed
        
    def get_deck_location(self):
        '''CardDeck.get_deck_location() -> (x,y)
        returns the location for the deck'''
        return self.deckLocation

    def get_discard_location(self):
        '''CardDeck.get_discard_location() -> (x,y)
        returns the location for the discard pile'''
        return self.discardLocation

    def set_deck_location(self, newLocation):
        '''CardDeck.set_deck_location((x,y)) -> None
        sets the location of the card deck'''
        self.deckLocation = newLocation
        for card in self.deck:
            card.pos(self.deckLocation)

    def set_discard_location(self, newLocation, relative = True, sys = False):
        '''CardDeck.set_discard_location((x,y), relative = True) -> None
        sets the discard location
        relative controls whether this location will be relative to the deck location'''
        self.hasMovedDiscard = not sys
        if relative:
            self.discardLocation = self.deckLocation[0] + newLocation[0], self.deckLocation[1] + newLocation[1]
        else:
            self.discardLocation = newLocation
        for card in self.discard:
            card.pos(self.discardLocation)

    def get_deck(self):
        '''CardDeck.get_deck() -> list
        returns the deck of Card objects'''
        return self.deck

    def get_discard(self):
        '''CardDeck.get_discard() -> list
        returns the discard pile of Card objects'''
        return self.discard

    def set_discard(self, newDiscard):
        '''CardDeck.set_discard(Card[]) -> None
        sets the discard pile with a list of Card objects'''
        self.discard = newDiscard

    def set_deck(self, newDeck):
        '''CardDeck.set_deck(Card[]) -> None
        sets the deck with a list of Card objects'''
        self.unbind_deck_click()
        self.deck = newDeck
        self.rebind_deck_click()

    def load_deck(self, size = "medium", backColor = (21, 60, 129), outlineColor = (50,50,50),
            outlineWidth = 2, preloadDeck = None, includeJokers = True,
            visualStackHeight = 3, showEmptyPiles = True, preshuffle = True):
        '''CardDeck.load_deck(str, (x,y), (r,g,b), (r,g,b), int, bool, bool) -> None
        Loads a new deck of cards or generates a new deck with or without jokers
        If newDeck is None, a new full deck will be created
        If newDeck is provided, the deck is loaded from that
        A single card should look this: (face, suit, color) or ("10", "heart", "red")'''
        self.unbind_deck_click()
        self.deck.clear()
        self.discard.clear()

        self.visualStackHeight = visualStackHeight
        self.showEmptyPiles = showEmptyPiles
            
        if preloadDeck == None:
            faces = get_faces()
            suits = get_suits()
            colors = ["red", "black"]

            # load each card
            for face in faces:
                for suit in suits:
                    self.deck.append(
                        Card(self.game,(face, suit, colors[suits.index(suit) % 2]), size, backColor, outlineColor, outlineWidth)
                    )
                    
            # now add jokers
            if includeJokers:
                for color in colors:
                    self.deck.append(
                        Card(self.game,("JOKER", "JOKER", color), size, backColor, outlineColor, outlineWidth)
                    )
        else:
            for card in preloadDeck:
                self.deck.append(
                    Card(self.game, card, size, backColor, outlineColor, outlineWidth)
                )

        # set the location of all new cards
        self.size = size
        self.outlineWidth = outlineWidth
        self.set_deck_location(self.deckLocation)
        if not self.hasMovedDiscard:
            self.set_discard_location((get_sizes(outlineWidth)[self.size][0] * 1.15,0), True, True)
        self.redo_deck_stack_visual()

        # the size for the two empty cards (omne for the deck and one for discard
        w, h = get_sizes()[self.size]
        w *= 0.9
        h *= 0.9
        x1, y1 = self.discardLocation
        x2, y2 = self.deckLocation

        # build the two empty cards
        self.discardEmpty = Card(self.game, ("EMPTY", "heart", "red"), size, outlineColor = (130,130,130), outlineWidth = 2)
        self.discardEmpty.pos(self.discardLocation)
        self.discardEmpty.flip_card()
        self.deckEmpty = Card(self.game, ("EMPTY", "heart", "red"), size, outlineColor = (130,130,130), outlineWidth = 2)
        self.deckEmpty.pos(self.deckLocation)
        self.deckEmpty.flip_card()

        if preshuffle:
            self.shuffle_deck()

    def onclick(self, command = None):
        '''CardDeck.onclick(command = None) -> None
        sets what happens when you click the top card of the deck
        if set to None, nothing will happen when card is clicked'''
        self.unbind_deck_click()
        self.eventCommand = command
        self.rebind_deck_click()
        
    def shuffle_deck(self):
        '''CardDeck.shuffle_deck() -> None
        shuffles the current deck'''
        self.unbind_deck_click()
        random.shuffle(self.deck)
        self.rebind_deck_click()
        self.redo_deck_stack_visual()

    def get_top_of_deck(self):
        '''CardDeck.get_top_of_deck() -> Card
        returns the card on top of the card deck
        This card is the first element in the deck list'''
        if len(self.deck) == 0: return
        return self.deck[0]

    def pop_top_of_deck(self):
        '''CardDeck.pop_top_of_deck() -> Card
        removes the card on top of the card deck (first element)
        returns the removed card'''
        if len(self.deck) == 0: return
        self.unbind_deck_click()
        output = self.deck.pop(0)
        self.rebind_deck_click()
        self.redo_deck_stack_visual()
        return output

    def get_top_of_discard(self):
        '''CardDeck.get_top_of_discard() -> Card
        returns the card on top of the discard
        This is the last element in the discard list'''
        if len(self.discard) == 0: return
        return self.discard[-1]

    def pop_top_of_discard(self):
        '''CardDeck.pop_top_of_discard() -> Card
        removes the card on top of the discard (last element)
        returns the removed card'''
        if len(self.discard) == 0: return
        self.redo_discard_stack_visual()
        return self.discard.pop()

    def unbind_deck_click(self):
        '''CardDeck.unbind_deck_click() -> None
        unbinds the one event attached to the card deck
        function that was called is CardDeck.process_click_of_top_card'''
        if len(self.deck) > 0:
            self.get_top_of_deck().remove_event("on-deck-click")

    def rebind_deck_click(self):
        '''CardDeck.rebind_deck_click(self):
        rebinds the one event attached to the card deck
        function called is CardDeck.process_click_of_top_card'''
        if len(self.deck) > 0 and self.eventCommand != None:
            self.get_top_of_deck().onclick("on-deck-click", self.eventCommand)

    def restack(self):
        '''CardDeck.restack() -> None
        restacks the deck with the discard pile
        the discard is added to the bottom of the deck'''
        self.deck.extend(self.discard)
        self.discard.clear()
        self.redo_deck_stack_visual()

    def add_card_to_deck(self, card):
        '''CardDeck.add_card_to_deck(Card) -> None
        adds a card to the BOTTOM of the deck
        accomblished by adding it to the end of the list'''
        self.deck.append(card)
        self.redo_deck_stack_visual()

    def add_card_to_discard(self, card):
        '''CardDeck.add_card_to_discard(Card) -> None
        adds a card to the TOP of the discard pile
        accomblished by adding it to the end of the list'''
        self.discard.append(card)
        self.redo_discard_stack_visual()

    def process_click_of_top_card(self, event):
        '''CardDeck.process_click_of_top_card(event) -> None
        This is called whenever the top card in the deck is clicked'''
        card = self.get_top_of_deck()
        if card != None:
            self.unbind_deck_click()

            # determine where to put the card and stick respect the stack visual
            if len(self.discard) < 1:
                moveTo = self.discardLocation
            elif len(self.discard) < self.visualStackHeight - 1:
                moveTo = (self.discardLocation[0] - self.outlineWidth * 2 * len(self.discard),
                    self.discardLocation[1] - self.outlineWidth * 2 * len(self.discard))
            else:
                moveTo = (self.discardLocation[0] - self.outlineWidth * 2 * (self.visualStackHeight - 1),
                    self.discardLocation[1] - self.outlineWidth * 2 * (self.visualStackHeight - 1))

            # move the card and then flip it after it stops moving
            timeToMove = card.move_to(moveTo, self.movementSpeed)
            self.game.after(timeToMove + 100, self.discard_top_card)

    def discard_top_card(self, animateFlip = True):
        '''CardDeck.discard_top_card(animateFlip = True) -> None
        moves the top card of the deck to the top of the discard
        if animateFlip is True, Card.shake_flip() is used
        otherwise Card.flip_card() is used'''
        card = self.pop_top_of_deck()
        self.add_card_to_discard(card)
        if animateFlip:
            card.shake_flip()
        else:
            card.flip_card()

    def redo_deck_stack_visual(self):
        '''CardDeck.redo_deck_stack_visual() -> None
        goes through all cards in the deck and creates the stack visual offset
        this is to give the pile a 3Dish look
        called after a change in the deck to redo the visual'''
        for i in range(len(self.deck)):
            visualHeight = min(self.visualStackHeight - 1, len(self.deck) - i - 1)
            self.deck[i].pos((
                self.deckLocation[0] - self.outlineWidth * 2 * visualHeight,
                self.deckLocation[1] - self.outlineWidth * 2 * visualHeight
            ))

    def redo_discard_stack_visual(self):
        '''CardDeck.redo_discard_stack_visual() -> None
        goes through all cards in the discard and creates the stack visual offset
        this is to give the pile a 3Dish look
        called after a change in the discard to redo the visual'''
        for i in range(len(self.discard)):
            visualHeight = min(self.visualStackHeight - 1, i)
            self.discard[i].pos((
                self.discardLocation[0] - self.outlineWidth * 2 * visualHeight,
                self.discardLocation[1] - self.outlineWidth * 2 * visualHeight
            ))

    def update(self):
        '''CardDeck.update() -> None
        renders and updates the card deck'''
        
        # draw the discard pile
        if len(self.discard) == 0 and self.showEmptyPiles:
            self.discardEmpty.update()
        else:
            for i in range(len(self.discard)):
                self.discard[i].update()

        # draw the deck
        if len(self.deck) == 0 and self.showEmptyPiles:
            self.deckEmpty.update()
        else:
            for j in range(len(self.deck)-1, -1, -1):
                self.deck[j].update()

class _TestGame(gs.Game):
    ''' quick test game for the cards and card deck'''

    def __init__(self):
        gs.Game.__init__(self, (1200,800), bg=(255,255,255))

        self.decks = []
        self.decks.append(CardDeck(self, (900,650), size="large", backColor=get_colors()["purple"]))
        self.decks.append(CardDeck(self, (700, 590), size="tiny",
            backColor=get_colors()["gold"], preloadDeck = [("JOKER", "JOKER", "red")]))
        self.decks.append(CardDeck(self, (700, 710), size="tiny", backColor=get_colors()["red"]))
        self.decks.append(CardDeck(self, (470, 650), size="medium", backColor=get_colors()["green"]))
        self.decks.append(CardDeck(self, (250, 580), size="small", backColor=get_colors()["pink"]))
        self.decks.append(CardDeck(self, (250, 720), size="small", backColor=get_colors()["silver"]))
        self.decks.append(CardDeck(self, (75, 580), size="small", backColor=get_colors()["orange"]))
        self.decks.append(CardDeck(self, (75, 720), size="small", backColor=get_colors()["blue"]))
        self.decks[-1].onclick(self.decks[-1].get_top_of_deck()._event_flip)

        topRow = [("4", "club", "black"), ("10", "spade", "black"),
            ("K", "diamond", "red"), ("A", "heart", "red"), ("JOKER", "JOKER", "red"),
            ("6", "club", "black"), ("J", "heart", "red"), ("2", "spade", "black"), ("7", "diamond", "red")]
        self.cards = []
        x = 120
        for card in topRow:
            newCard = Card(self, card, size="medium", backColor=get_colors()["green"])
            newCard.pos((x,100))
            if random.random() > 0.3: newCard.flip_card()
            newCard.onclick(None, newCard._event_flip)
            x += 120
            self.cards.append(newCard)

        large = [("Q", "spade", "black"), ("4", "diamond", "red"), ("10", "heart", "red")]
        x = 130
        for card in large:
            newCard = Card(self, card, size="large", backColor=get_colors()["pink"])
            newCard.pos((x,345))
            if random.random() > 0.3: newCard.flip_card()
            newCard.onclick(None, newCard._event_flip)
            x += 170
            self.cards.append(newCard)

        small = [("JOKER", "JOKER", "black"), ("A", "spade", "black"),
            ("5", "heart", "red"), ("9", "diamond", "red")]
        x = 650
        for card in small:
            newCard = Card(self, card, size="medium", backColor=get_colors()["yellow"])
            newCard.pos((x,290))
            if random.random() > 0.3: newCard.flip_card()
            newCard.onclick(None, newCard._event_flip)
            x += 125
            self.cards.append(newCard)

        tiny = [("K", "heart", "red"), ("6", "club", "black"),
            ("9", "diamond", "red"), ("Q", "club", "black"), ("8", "club", "black"),
            ("7", "diamond", "red"), ("A", "spade", "black"), ("Q", "heart", "red"),
            ("2", "diamond", "red"), ("3", "club", "black")]
        x = 605
        for card in tiny:
            newCard = Card(self, card, size="tiny", backColor=get_colors()["orange"])
            newCard.pos((x,445))
            if random.random() > 0.3: newCard.flip_card()
            newCard.onclick(None, newCard._event_flip)
            x += 60
            self.cards.append(newCard)

    def update(self):
        for deck in self.decks:
            deck.update()
        for card in self.cards:
            card.update()

def version():
    '''version() -> str
    returns the playingcard module version'''
    return GAME_VERSION

def get_suits():
    '''get_suits() -> ["heart", "spade", "diamond", "club"]
    returns a list of all suits
    jokers not includes'''
    return ["heart", "spade", "diamond", "club"]

def get_faces():
    '''get_faces() -> ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    returns a list of all faces
    jokers not includes'''
    return ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

def get_sizes(outlineWidth = 0):
    '''get_sizes(int) -> dict
    returns a dictionary with the widths and heights for all sizes
    sizes are: "tiny", "small", "medium", and "large"
    adjusts for the given outline width'''
    smallWidth = 70
    ratio = 1.5
    return {
        "tiny": (smallWidth/ratio + outlineWidth*2, smallWidth + outlineWidth*2),
        "small": (smallWidth + outlineWidth*2, smallWidth*ratio + outlineWidth*2),
        "medium": (smallWidth*ratio + outlineWidth*2, smallWidth*ratio**2 + outlineWidth*2),
        "large": (smallWidth*ratio**2 + outlineWidth*2, smallWidth*ratio**3 + outlineWidth*2)
    }

def get_colors():
    '''get_colors() -> dict
    returns a dictionary of colors with some good choices for the back of the card
    includes "red", "orange", "yellow", "green", "blue", "purple", "pink", "silver", and "gold"'''
    return {
        "red": (170, 0, 0),
        "orange": (242, 82,15),
        "yellow": (225, 188, 35),
        "green": (81, 149, 69),
        "blue": (21, 60, 129),
        "purple": (96, 51, 169),
        "pink": (226, 63, 98),
        "silver": (145, 148, 156),
        "gold": (222, 179, 97),
    }        
            
# test the cards
if __name__ == "__main__":
    pygame.init()
    game = _TestGame()
    game.mainloop()
    
    
