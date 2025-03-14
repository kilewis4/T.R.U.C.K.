import simpy
from Truck import Truck
from UnloadingProcess import unloading
from TruckList import TruckList
from UnloaderList import UnloaderList
from DoorList import DoorList

import threading
import time

import pygame as pg
import tkinter as tk


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

class GUI():
    def __init__(self):
        
        self.env = simpy.RealtimeEnvironment()
        self.incomingTrucks = []
        self.trucks = TruckList(self.env)
        self.unloaders = UnloaderList(self.env)
        self.doors = DoorList()

        self.truck_graphics = []

    def animation(self):

        door_graphics = []
        for door in self.doors.list:
            door_graphics.append(door.number)

        self.env.process(self.process_manager())
        sim_thread = threading.Thread(target=self.run_simulation, daemon=True)
        sim_thread.start()

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
        DOOR_YPOSITION = SCREEN_HEIGHT / (len(door_graphics) + 1)

        # Creates display and sets caption.
        DISPLAYSURF = pg.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption('OVERVIEW SCREEN')

        # Creates two different color schemes to use for when use clicks on text input.
        inactive_color = pg.Color('lightskyblue3')
        active_color = pg.Color('dodgerblue2')
        po_text_box_color = inactive_color
        size_text_box_color = inactive_color
        live_text_box_color = inactive_color
        # Default text input is nothing.
        po_text = ''
        size_text = ''
        live_text = ''

        po_text_box_active = False
        size_text_box_active = False
        live_text_box_active = False

        # Creates dimensions for text input.
        po_input_box = pg.Rect(SCREEN_WIDTH - (SCREEN_WIDTH / 4), 0, (140), 32)
        size_input_box = pg.Rect(SCREEN_WIDTH - (SCREEN_WIDTH / 4), 64, (140), 32)
        live_input_box = pg.Rect(SCREEN_WIDTH - (SCREEN_WIDTH / 4), 128, (140), 32)
        button = pg.Rect(SCREEN_WIDTH - (SCREEN_WIDTH / 4), 192, (140), 32)

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if button.collidepoint(event.pos):
                        new_truck = Truck(
                            int(po_text),
                            int(size_text),
                            0,
                            self.env.now
                        )
                        self.add_truck(self.env, new_truck)
                        time.sleep(2)
                    if po_input_box.collidepoint(event.pos):
                        po_text_box_active = True
                    else:
                        po_text_box_active = False
                    
                    if size_input_box.collidepoint(event.pos):
                        size_text_box_active = True
                    else:
                        size_text_box_active = False

                    if live_input_box.collidepoint(event.pos):
                        live_text_box_active = True
                    else:
                        live_text_box_active = False

                    po_text_box_color = active_color if po_text_box_active else inactive_color
                    size_text_box_color = active_color if size_text_box_active else inactive_color
                    live_text_box_color = active_color if live_text_box_active else inactive_color
                
                if event.type == pg.KEYDOWN:
                    if po_text_box_active:
                        if event.key == pg.K_BACKSPACE:
                            po_text = po_text[:-1]
                        else:
                            po_text += event.unicode
                    
                    if size_text_box_active:
                        if event.key == pg.K_BACKSPACE:
                            size_text = size_text[:-1]
                        else:
                            size_text += event.unicode
                    
                    if live_text_box_active:
                        if event.key == pg.K_BACKSPACE:
                            live_text = size_text[:-1]
                        else:
                            live_text += event.unicode
            
            DISPLAYSURF.fill(WHITE)

            
            button_text_surface = font.render("Submit", True, BLACK)
            DISPLAYSURF.blit(button_text_surface, (button.x+5, button.y+5))
            pg.draw.rect(DISPLAYSURF, BLACK, button, 2)

            po_text_surface = font.render(po_text, True, po_text_box_color)
            DISPLAYSURF.blit(po_text_surface, (po_input_box.x+5, po_input_box.y+5))
            pg.draw.rect(DISPLAYSURF, po_text_box_color, po_input_box, 2)

            size_text_surface = font.render(size_text, True, size_text_box_color)
            DISPLAYSURF.blit(size_text_surface, (size_input_box.x+5, size_input_box.y+5))
            pg.draw.rect(DISPLAYSURF, size_text_box_color, size_input_box, 2)

            live_text_surface = font.render(live_text, True, live_text_box_color)
            DISPLAYSURF.blit(live_text_surface, (live_input_box.x+5, live_input_box.y+5))
            pg.draw.rect(DISPLAYSURF, live_text_box_color, live_input_box, 2)

            idx = 1
            for door in door_graphics:
                door_graphic = pg.Rect(DOOR_XPOSITION, DOOR_YPOSITION * idx, 40, 40)
                pg.draw.rect(DISPLAYSURF, RED, door_graphic)
                idx += 1
            
            self.draw_trucks(self.truck_graphics, DISPLAYSURF)
            self.update_trucks(self.truck_graphics, DOOR_XPOSITION, DOOR_YPOSITION)
            
            pg.display.flip()
            clock.tick(30)
        
        print("End time: " + self.env.now)


    def update_trucks(self, trucks, DOOR_XPOSITION, DOOR_YPOSITION):
        for truck in trucks:
            print(truck)
            if truck.reached_door and truck.done:
                truck.go_out()
            else:
                truck.go_in(DOOR_XPOSITION, DOOR_YPOSITION)

    def draw_trucks(self, trucks, surface):
        for truck in trucks:
            truck_object = pg.Rect(truck.truck_x_position, truck.truck_y_position, 50, 25)
            pg.draw.rect(surface, GREEN, truck_object)

    """ Runs simulation
        Prints the start time and than runs the global enviroment.
    """
    def run_simulation(self):
        print('The start time is: ' + str(self.env.now))
        self.env.run()

    """ Manages the incoming trucks being processed
        When new truck arrives adds it to the simulation and begins process.
    """
    def process_manager(self):
        """Constantly checks for new processes while keeping the simulation running"""
        while True:
            if self.incomingTrucks:
                nextTruck = self.incomingTrucks.pop(0)
                print(str(nextTruck.po) + " has arrived at " + str(nextTruck.time) + " size: " + str(nextTruck.size) + " env time: " + str(self.env.now))
                self.trucks.addTruck(nextTruck, self.env)
                self.env.process(unloading(self))
            yield self.env.timeout(1)

    """ Adds truck
        Adds inputted truck to incoming trucks list.
    """
    def add_truck(self, env, truck):
        self.incomingTrucks.append(truck)

    def add_truck_graphic(self, truck_graphic):
        self.truck_graphics.append(truck_graphic)
    


gui = GUI()
gui.animation()