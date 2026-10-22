import pygame

leftKey = pygame.K_a
rightKey = pygame.K_d
upKey = pygame.K_w
downKey = pygame.K_s



class GameLogic:

    leftArrow = pygame.image
    rightArrow = pygame.image
    upArrow = pygame.image
    downArrow = pygame.image
    distanceBetweenArrows = 110
    arrowsPosY = 100

    def __init__(self):

        print("Game Logic Assets initialised")
        self.leftArrow  =  pygame.image.load("assets/leftArrow.png")
        self.rightArrow = pygame.image.load("assets/rightArrow.png")
        self.upArrow    =    pygame.image.load("assets/upArrow.png")
        self.downArrow  =  pygame.image.load("assets/downArrow.png")

        self.PressedLeftArrow   =   pygame.image.load("assets/PressedleftArrow.png")
        self.PressedRightArrow  =  pygame.image.load("assets/PressedrightArrow.png")
        self.PressedUpArrow     =     pygame.image.load("assets/PressedupArrow.png")
        self.PressedDownArrow   =   pygame.image.load("assets/PresseddownArrow.png")


        pass

    def update(self, screen):
        keys = pygame.key.get_pressed()

        screen.blit(self.leftArrow,  (700,                                  self.arrowsPosY))
        screen.blit(self.downArrow,  (700 + self.distanceBetweenArrows,     self.arrowsPosY))
        screen.blit(self.upArrow,    (700 + self.distanceBetweenArrows * 2, self.arrowsPosY))
        screen.blit(self.rightArrow, (700 + self.distanceBetweenArrows * 3, self.arrowsPosY))


        if keys[leftKey]:
            screen.blit(self.PressedLeftArrow, (700, self.arrowsPosY))
            print("LEFT")


        if keys[rightKey]:
            screen.blit(self.PressedRightArrow, (700 + self.distanceBetweenArrows * 3, self.arrowsPosY))
            print("RIGHT")


        if keys[upKey]:
            screen.blit   (self.PressedUpArrow, (700 + self.distanceBetweenArrows * 2, self.arrowsPosY))
            print("UP")


        if keys[downKey]:
            screen.blit (self.PressedDownArrow, (700 + self.distanceBetweenArrows * 1, self.arrowsPosY))
            print("DOWN")
