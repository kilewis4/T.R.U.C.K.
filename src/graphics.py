import pygame as pg
import tkinter as tk
from Door import Door
from Truck import Truck

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

def animation(doors):
    # Create text on screen for inputting door numbers.
    pg.font.init()
    font = pg.font.SysFont(None, 18)
    clock = pg.time.Clock()

    # Sets screen size relative to size of users monitor.
    ROOT = tk.Tk()
    SCREEN_WIDTH = ROOT.winfo_screenwidth() - 100
    SCREEN_HEIGHT = ROOT.winfo_screenheight() - 100

    # Finds initial x, y position for doors.
    DOOR_XPOSITION = SCREEN_WIDTH / 2
    DOOR_YPOSITION = SCREEN_HEIGHT / (len(doors) + 1)

    # Creates display and sets caption.
    DISPLAYSURF = pg.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('OVERVIEW SCREEN')

    # Creates two different color schemes to use for when use clicks on text input.
    inactive_color = pg.Color('lightskyblue3')
    active_color = pg.Color('dodgerblue2')
    text_box_color = active_color
    # Default text input is nothing.
    text = ''
    text_box_active = False

    # Creates dimensions for text input.
    input_box = pg.Rect(SCREEN_WIDTH - (SCREEN_WIDTH / 4), 0, 140, 32)

    trucks = []

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    text_box_active = True
                else:
                    text_box_active = False
                text_box_color = active_color if text_box_active else inactive_color
            if event.type == pg.KEYDOWN:
                if text_box_active:
                    if event.key == pg.K_RETURN:
                        print(text)
                        trucks.append(TruckGraphic(int(text)))
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        
        DISPLAYSURF.fill(WHITE)

        text_surface = font.render(text, True, text_box_color)
        DISPLAYSURF.blit(text_surface, (input_box.x+5, input_box.y+5))
        pg.draw.rect(DISPLAYSURF, text_box_color, input_box, 2)

        idx = 1
        for door in doors:
            door_graphic = pg.Rect(DOOR_XPOSITION, DOOR_YPOSITION * idx, 40, 40)
            pg.draw.rect(DISPLAYSURF, RED, door_graphic)
            idx += 1
        
        draw_trucks(trucks, DISPLAYSURF)
        update_trucks(trucks, DOOR_XPOSITION, DOOR_YPOSITION)
        
        pg.display.flip()
        clock.tick(30)


def update_trucks(trucks, DOOR_XPOSITION, DOOR_YPOSITION):
    for truck in trucks:
        if truck.reached_door:
            truck.go_out()
        else:
            truck.go_in(DOOR_XPOSITION, DOOR_YPOSITION)

def draw_trucks(trucks, surface):
    for truck in trucks:
        truck_object = pg.Rect(truck.truck_x_position, truck.truck_y_position, 50, 25)
        pg.draw.rect(surface, GREEN, truck_object)


class TruckGraphic():
    def __init__(self, door_num):
        self.truck_x_position = 0
        self.truck_y_position = 0
        self.door_num = door_num
        self.reached_door = False
        
    
    def go_in(self, DOOR_XPOSITION, DOOR_YPOSITION):
        if self.truck_x_position == DOOR_XPOSITION - 50 and self.truck_y_position == DOOR_YPOSITION * self.door_num:
            self.reached_door = True
        else:
            if self.truck_x_position < DOOR_XPOSITION - 50:
                self.truck_x_position += 5
            if self.truck_y_position < DOOR_YPOSITION * self.door_num:
                self.truck_y_position += 5
    
    def go_out(self):
        if self.truck_x_position > -100:
            self.truck_x_position -= 5
    
animation([Door(1), Door(2), Door(3)])



