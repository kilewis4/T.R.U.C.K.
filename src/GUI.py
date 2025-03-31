import simpy
from Truck import Truck
from UnloadingProcess import unloading
from TruckList import TruckList
from UnloaderList import UnloaderList
from DoorList import DoorList
from UnloaderGraphic import UnloaderGraphic

import threading
import time
import math
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
        self.unloader_graphics = []
        self.text_lines = []
        

        

    def animation(self):
        door_graphics = []
        for door in self.doors.list:
            door_graphics.append(door.number)

        terminal_boxes = []


        self.env.process(self.process_manager())
        sim_thread = threading.Thread(target=self.run_simulation, daemon=True)
        sim_thread.start()

        # Create text on screen for inputting door numbers.
        pg.font.init()
        self.FONT_SIZE = 18
        font = pg.font.SysFont(None, self.FONT_SIZE)
        clock = pg.time.Clock()

        # Sets screen size relative to size of users monitor.
        ROOT = tk.Tk()
        self.SCREEN_WIDTH = ROOT.winfo_screenwidth() - 100
        self.SCREEN_HEIGHT = ROOT.winfo_screenheight() - 100

        UNLOADERS_WAITLIST_X = self.SCREEN_WIDTH * 3/4
        UNLOADERS_WAITLIST_Y = self.SCREEN_HEIGHT * 3/4

        UNLOADERS_INBETWEEN = (self.SCREEN_HEIGHT * 1/4) / len(self.unloaders.list)

        for unloader in self.unloaders.list:
            unloader_graphic = UnloaderGraphic(unloader.eid, math.floor(UNLOADERS_WAITLIST_X), math.floor(UNLOADERS_WAITLIST_Y))
            self.unloader_graphics.append(unloader_graphic)
            UNLOADERS_WAITLIST_Y += UNLOADERS_INBETWEEN

        # Finds initial x, y position for doors.
        DOOR_XPOSITION = self.SCREEN_WIDTH / 2
        DOOR_YPOSITION = self.SCREEN_HEIGHT / (len(door_graphics) + 1)

        # Creates display and sets caption.
        DISPLAYSURF = pg.display.set_mode(size=(self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pg.display.set_caption('OVERVIEW SCREEN')

        # Creates two different color schemes to use for when use clicks on text input.
        inactive_color = pg.Color('BLACK')
        active_color = pg.Color('dodgerblue2')
        po_text_box_color = inactive_color
        size_text_box_color = inactive_color

        live_true_box_color = inactive_color
        live_false_box_color = inactive_color

        #live_text_box_color = inactive_color
        # Default text input is nothing.
        po_text = ''
        size_text = ''
        #live_text = ''

        po_text_box_active = False
        size_text_box_active = False
        self.live_text_box_active = False
        live_true_box_active = False
        live_false_box_active = False

        input_background = pg.Rect(self.SCREEN_WIDTH - 300, 0, 300, 300)
        terminal_background = pg.Rect(0, self.SCREEN_HEIGHT - 300, 350, 300)

        self.lines = []
        self.max_lines = 300 // self.FONT_SIZE


        # Creates dimensions for text input.
        po_input_box = pg.Rect(self.SCREEN_WIDTH - 200, 10, (140), 32)
        po_label_box = pg.Rect(po_input_box.x - 40, po_input_box.y + 8, 32, 32)
        size_input_box = pg.Rect(self.SCREEN_WIDTH - 200, 74, (140), 32)
        size_label_box = pg.Rect(size_input_box.x - 90, size_input_box.y + 8, 32, 32)
        #live_input_box = pg.Rect(SCREEN_WIDTH - 200, 138, (140), 32)

        live_true_button = pg.Rect(self.SCREEN_WIDTH - 200, 138, 70, 32)
        live_false_button = pg.Rect(self.SCREEN_WIDTH - 125, 138, 70, 32)
        live_label_box = pg.Rect(live_true_button.x - 40, live_true_button.y + 8, 32, 32)
            

        

        button = pg.Rect(self.SCREEN_WIDTH - 200, 202, (140), 32)

        live_input_box = pg.Rect(self.SCREEN_WIDTH - 200, 138, (140), 32)
        live_label_box = pg.Rect(live_input_box.x - 40, live_input_box.y + 8, 32, 32)
        button = pg.Rect(self.SCREEN_WIDTH - 200, 202, (140), 32)

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if button.collidepoint(event.pos):
                        live_value = 0
                        if live_true_box_active:
                            live_value = 1
                        new_truck = Truck(
                            int(po_text),
                            int(size_text),
                            live_value,
                            self.env.now
                        )
                        self.add_truck(self.env, new_truck)
                
                        
                        
                    if po_input_box.collidepoint(event.pos):
                        po_text_box_active = True
                    else:
                        po_text_box_active = False
                    
                    if size_input_box.collidepoint(event.pos):
                        size_text_box_active = True
                    else:
                        size_text_box_active = False

                    if live_true_button.collidepoint(event.pos):
                        live_true_box_active = True
                        live_false_box_active = False
                        
                    if live_false_button.collidepoint(event.pos):
                        live_false_box_active = True
                        live_true_box_active = False

                    po_text_box_color = active_color if po_text_box_active else inactive_color
                    size_text_box_color = active_color if size_text_box_active else inactive_color
                    live_true_box_color = active_color if live_true_box_active else inactive_color
                    live_false_box_color = active_color if live_false_box_active else inactive_color
                
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
                    

                    if self.live_text_box_active:
                        if event.key == pg.K_BACKSPACE:
                            live_text = live_text[:-1]

                        else:
                            live_text += event.unicode
            
            DISPLAYSURF.fill(GRAY)

            pg.draw.rect(DISPLAYSURF, GRAY, input_background)
            
            button_text_surface = font.render("Submit", True, BLACK)
            DISPLAYSURF.blit(button_text_surface, (button.x+5, button.y+5))
            pg.draw.rect(DISPLAYSURF, BLACK, button, 2)

            po_text_surface = font.render(po_text, True, po_text_box_color)
            DISPLAYSURF.blit(po_text_surface, (po_input_box.x+5, po_input_box.y+5))
            pg.draw.rect(DISPLAYSURF, po_text_box_color, po_input_box, 2)

            po_label_surface = font.render('PO #:', True, WHITE)
            DISPLAYSURF.blit(po_label_surface, (po_label_box.x, po_label_box.y))

            size_text_surface = font.render(size_text, True, size_text_box_color)
            DISPLAYSURF.blit(size_text_surface, (size_input_box.x+5, size_input_box.y+5))
            pg.draw.rect(DISPLAYSURF, size_text_box_color, size_input_box, 2)

            size_label_surface = font.render('# OF PALLETS:', True, WHITE)
            DISPLAYSURF.blit(size_label_surface, (size_label_box.x, size_label_box.y))

            live_true_text_surface = font.render('YES', True, live_true_box_color)
            DISPLAYSURF.blit(live_true_text_surface, (live_true_button.x+25, live_true_button.y+10))
            pg.draw.rect(DISPLAYSURF, live_true_box_color, live_true_button, 2)

            live_false_text_surface = font.render('NO', True, live_false_box_color)
            DISPLAYSURF.blit(live_false_text_surface, (live_false_button.x+25, live_false_button.y+10))
            pg.draw.rect(DISPLAYSURF, live_false_box_color, live_false_button, 2)

            live_label_surface = font.render('LIVE:', True, WHITE)
            DISPLAYSURF.blit(live_label_surface, (live_label_box.x, live_label_box.y))

            warehouse_outline_left = pg.Rect(DOOR_XPOSITION, 75, 5, self.SCREEN_HEIGHT - 100)
            pg.draw.rect(DISPLAYSURF, BLACK, warehouse_outline_left)

            warehouse_outline_top = pg.Rect(DOOR_XPOSITION, 75, 275, 5)
            pg.draw.rect(DISPLAYSURF, BLACK, warehouse_outline_top)

            warehouse_outline_bottom = pg.Rect(DOOR_XPOSITION, self.SCREEN_HEIGHT - 25, 275, 5)
            pg.draw.rect(DISPLAYSURF, BLACK, warehouse_outline_bottom)

            idx = 1
            for door in door_graphics:
                door_text_surface = font.render(str(idx), True, BLACK)
                door_graphic = pg.Rect(DOOR_XPOSITION, DOOR_YPOSITION * idx, 40, 40)
                pg.draw.rect(DISPLAYSURF, RED, door_graphic)
                DISPLAYSURF.blit(door_text_surface, (DOOR_XPOSITION + 15, DOOR_YPOSITION * idx + 15))
                idx += 1

            for unloader in self.unloader_graphics:
                unloader_text_surface = font.render(str(unloader.eid), True, WHITE)
                unloader_graphic = pg.draw.circle(DISPLAYSURF, BLACK, (unloader.x_position, unloader.y_position), 10)
                DISPLAYSURF.blit(unloader_text_surface, (unloader.x_position - 5, unloader.y_position - 5))
                

            
            self.draw_trucks(self.truck_graphics, DISPLAYSURF, font)
            self.update_trucks(self.truck_graphics, DOOR_XPOSITION, DOOR_YPOSITION)
            self.update_unloaders(DOOR_XPOSITION, DOOR_YPOSITION)
            self.draw_terminal(DISPLAYSURF, terminal_background, font)            



            
            
            pg.display.flip()
            clock.tick(30)
        
        print("End time: " + str(self.env.now))

    
    def update_unloaders(self, DOOR_XPOSITION, DOOR_YPOSITION):
        for unloader_graphic in self.unloader_graphics:
            if unloader_graphic.current_door != -1:
                if not unloader_graphic.reached_door:
                    unloader_graphic.go_in(DOOR_XPOSITION, DOOR_YPOSITION * unloader_graphic.current_door)
            else:
                if unloader_graphic.initial_x != unloader_graphic.x_position or unloader_graphic.initial_y != unloader_graphic.y_position:
                    unloader_graphic.go_out()
                    unloader_graphic.reached_door = False


    def update_trucks(self, trucks, DOOR_XPOSITION, DOOR_YPOSITION):
        for truck in trucks:
            if truck.gone:
                trucks.remove(truck)
            elif truck.reached_door and truck.done:
                truck.go_out()
            else:
                truck.go_in(DOOR_XPOSITION, DOOR_YPOSITION)

    def draw_trucks(self, trucks, surface, font):
        for truck in trucks:
            truck_object = pg.Rect(truck.truck_x_position, truck.truck_y_position, 100, 25)
            truck_text_surface = font.render(str(truck.po_num), True, BLACK)
            pg.draw.rect(surface, WHITE, truck_object)
            surface.blit(truck_text_surface, (truck_object.x + (truck_object.width / 2), truck_object.y + (truck_object.height / 4)))

    def add_text(self, new_text):
        self.lines.append(new_text)
        if len(self.lines) > self.max_lines:
            self.lines.pop(0)

    def draw_terminal(self, DISPLAYSURF, terminal_background, font):
        pg.draw.rect(DISPLAYSURF, BLACK, terminal_background)
        y_offset = (terminal_background.y + 300) - (terminal_background.height / 300)
        y_offset -= self.FONT_SIZE

        for line in self.lines:
            text_surface = font.render(line, True, WHITE)  # Render text
            DISPLAYSURF.blit(text_surface, (0, y_offset))  # Draw text
            y_offset -= self.FONT_SIZE  # Move text down


    """ 
    Runs simulation
    Prints the start time and than runs the global enviroment.
    """
    def run_simulation(self):
        print('The start time is: ' + str(self.env.now))
        self.env.run()

    """ 
    Manages the incoming trucks being processed
    When new truck arrives adds it to the simulation and begins process.
    """
    def process_manager(self):
        #Constantly checks for new processes while keeping the simulation running
        while True:
            if self.incomingTrucks:
                nextTruck = self.incomingTrucks.pop(0)
                print(str(nextTruck.po) + " has arrived at " + str(nextTruck.time) + " size: " + str(nextTruck.size) + " env time: " + str(self.env.now))
                #self.add_text(f"Truck number {nextTruck.po} is arriving at time {nextTruck.time}")
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
    
    def assign_unloader(self, unloader_graphic, door_num):
        unloader_graphic.current_door = door_num
    
gui = GUI()
gui.animation()
