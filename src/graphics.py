import pygame, sys
import tkinter as tk
from Door import Door

def animation(doors):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    ROOT = tk.Tk()

    SCREEN_WIDTH = ROOT.winfo_screenwidth() - 100
    SCREEN_HEIGHT = ROOT.winfo_screenheight() - 100

    SQUARE_XPOSITION = SCREEN_WIDTH / 2
    SQUARE_YPOSITION = SCREEN_HEIGHT / len(doors)

    DISPLAYSURF = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Overview Screen")

    

    while True:
        DISPLAYSURF.fill(WHITE)
        i = 1
        for door in doors:
            rectangle = pygame.Rect(SQUARE_XPOSITION, SQUARE_YPOSITION * i, 40, 40)
            pygame.draw.rect(DISPLAYSURF, RED, rectangle)
            i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


animation({Door(1), Door(2), Door(3)})