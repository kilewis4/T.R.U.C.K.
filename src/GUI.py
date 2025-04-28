import simpy
from Truck import Truck
from UnloadingProcess import unloading
from TruckList import TruckList
from UnloaderList import UnloaderList
from DoorList import DoorList
from UnloaderGraphic import UnloaderGraphic
from DataVisualizer import visualize

import threading
import time
import math
import pygame as pg
import tkinter as tk

# Define basic color constants for use in graphical interface
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

""" 
Graphical User Interface (GUI)

This class serves as the driver for the program and provides an interactive interface for the user. 
It handles the simulation environment, truck arrivals, unloading processes, and rendering graphical elements. 

Attributes:
    env: simpy.RealtimeEnvironment object for simulation.
    incomingTrucks: List to store trucks that are to be processed.
    trucks: TruckList object to manage all trucks in the simulation.
    unloaders: UnloaderList object to manage all unloaders.
    doors: DoorList object for managing the warehouse doors.
    truck_graphics: List of truck graphic objects for display.
    unloader_graphics: List of unloader graphic objects for display.
    text_lines_scrollup: List of lines for the terminal’s scrolling text display.
    text_lines_scrolldown: List of lines for the terminal’s scrolling text display.
"""
class GUI():
    def __init__(self, experimental=False):
        """
        Initializes the GUI, including the simulation environment, truck list, unloader list, and door list.
        Sets up the graphical elements for trucks and unloaders.
        """
        self.env = simpy.RealtimeEnvironment()
        self.incomingTrucks = []
        self.experimental = experimental
        self.trucks = TruckList(self.env, experimental)
        self.unloaders = UnloaderList(self.env)
        self.doors = DoorList()

        self.truck_graphics = []
        self.unloader_graphics = []
        #self.text_lines_scrollup = []
        #self.text_lines_scrolldown = []
        if experimental:
            self.over_live_wait_time = 0


    def animation(self):
        """
        Main method to manage the graphical simulation, including the rendering of trucks, unloaders,
        and terminal output. It handles user interactions and processes the truck arrivals.
        """
        door_graphics = []
        for door in self.doors.list:
            door_graphics.append(door)

        self.terminal_boxes = []

        ROOT = tk.Tk()  # Initialize Tkinter window for screen size calculations
        self.SCREEN_WIDTH = ROOT.winfo_screenwidth() - 100 # Set screen width based on monitor size
        self.SCREEN_HEIGHT = ROOT.winfo_screenheight() - 100 # Set screen height based on monitor size
        ROOT.destroy()

        self.env.process(self.process_manager()) # Start the process manager in the simulation environment


        input_background = pg.Rect(self.SCREEN_WIDTH - 300, 0, 300, 300)
        terminal_background = pg.Rect(0, self.SCREEN_HEIGHT - 300, 350, 300)

        sim_thread = threading.Thread(target=self.run_simulation, daemon=True) # Run simulation in a separate thread
        sim_thread.start()

        # Create text on screen for inputting door numbers.
        pg.font.init()  # Initialize Pygame font system
        self.FONT_SIZE = 18
        font = pg.font.SysFont(None, self.FONT_SIZE)
        clock = pg.time.Clock() # Clock to manage FPS

        # Positioning for UI elements (e.g., text boxes, buttons)
        UNLOADERS_WAITLIST_X = self.SCREEN_WIDTH * 3/4
        UNLOADERS_WAITLIST_Y = self.SCREEN_HEIGHT * 3/4
        UNLOADERS_INBETWEEN = (self.SCREEN_HEIGHT * 1/4) / len(self.unloaders.list)

        for unloader in self.unloaders.list:
            # Initialize unloader graphics for each unloader
            unloader_graphic = UnloaderGraphic(unloader.eid, math.floor(UNLOADERS_WAITLIST_X), math.floor(UNLOADERS_WAITLIST_Y))
            self.unloader_graphics.append(unloader_graphic)
            UNLOADERS_WAITLIST_Y += UNLOADERS_INBETWEEN

        # Finds initial x, y position for doors.
        DOOR_XPOSITION = self.SCREEN_WIDTH / 2
        DOOR_YPOSITION = self.SCREEN_HEIGHT / (len(door_graphics) + 1)

        # Creates display and sets caption.
        DISPLAYSURF = pg.display.set_mode(size=(self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pg.display.set_caption('OVERVIEW SCREEN')

        # Creates two different color schemes to use for when user clicks on text input.
        inactive_color = pg.Color('BLACK')
        active_color = pg.Color('dodgerblue2')
        hover_inactive_color = GRAY
        hover_active_color = pg.Color('dodgerblue4')
        po_text_box_color = inactive_color
        size_text_box_color = inactive_color
        vendor_text_box_color = inactive_color

        # Color initialize for live box
        live_true_box_color = inactive_color
        live_false_box_color = inactive_color

        # Color initializse for sumbit button, and hovering for live
        submit_hover_color = hover_inactive_color
        live_true_hover_color = hover_inactive_color
        live_false_hover_color = hover_inactive_color
        reset_hover_color = hover_inactive_color
        

        # Default text input is nothing.
        po_text = ''
        size_text = ''
        vendor_text = ''

        # Boolean flags for active text input fields
        po_text_box_active = False
        size_text_box_active = False
        vendor_text_box_active = False
        self.live_text_box_active = False
        live_true_box_active = False
        live_false_box_active = False
        submit_hover_active = False
        live_true_hover_active = False
        live_false_hover_active = False
        reset_hover_active = False
        backspace_active = False

        # States for scroll.
        self.dragging = False
        self.drag_start_y = 0
        self.initial_scroll_offset = 0

        # Terminal setup for displaying simulation logs
        self.TERMINAL_WIDTH, self.TERMINAL_HEIGHT = 350, 300
        self.TERMINAL_X, self.TERMINAL_Y = self.SCREEN_WIDTH - 300, 0
        self.SCROLLBAR_WIDTH = 10
        self.scroll_offset = 0
        self.original_position = (0,0)

        # Lines in the terminal display
        self.lines = []
        #self.lines = [f"Line {i}" for i in range(50)]
        self.max_lines = self.TERMINAL_HEIGHT // self.FONT_SIZE


        # Creates dimensions for text input.
        po_input_box = pg.Rect(self.SCREEN_WIDTH - 200, 10, (155), 32)
        size_input_box = pg.Rect(self.SCREEN_WIDTH - 200, 54, (155), 32)
        vendor_input_box = pg.Rect(self.SCREEN_WIDTH - 200, 134, (155), 32)

        # Dimensions for True and False buttons.
        live_true_button = pg.Rect(self.SCREEN_WIDTH - 200, 94, 70, 32)
        live_false_button = pg.Rect(self.SCREEN_WIDTH - 115, 94, 70, 32)

        # Dimensions for highlighting effects,
        live_true_outline = pg.Rect(live_true_button.x-5, live_true_button.y-5, 80, 42)
        live_true_background = pg.Rect(live_true_button.x + 2, live_true_button.y + 2, (68), 30)
        
        live_false_outline = pg.Rect(live_false_button.x-5, live_false_button.y-5, 80, 42)
        live_false_background = pg.Rect(live_false_button.x + 2, live_false_button.y + 2, (68), 30)

    
        # Labels for input boxes.
        po_label_box = pg.Rect(po_input_box.x - 40, po_input_box.y + 8, 32, 32)
        size_label_box = pg.Rect(size_input_box.x - 90, size_input_box.y + 8, 32, 32)
        live_label_box = pg.Rect(live_true_button.x - 40, live_true_button.y + 8, 32, 32)
        vendor_label_box = pg.Rect(vendor_input_box.x - 68, vendor_input_box.y + 8, 32, 32)

        
        reset_button = pg.Rect(self.SCREEN_WIDTH - 200, 174, (52), 32)
        reset_button_outline = pg.Rect(reset_button.x-5, reset_button.y-5, reset_button.width + 10, reset_button.height + 10)
        reset_button_background = pg.Rect(reset_button.x + 2, reset_button.y+2, (reset_button.width)-2, reset_button.height-2)

        # Dimensions for Sumbit button
        button = pg.Rect(self.SCREEN_WIDTH - 98, 174, (52), 32)
        button_outline = pg.Rect(button.x-5, button.y-5, button.width + 10, button.height + 10)
        button_background = pg.Rect(button.x + 2, button.y+2, (button.width)-2, button.height-2)

        # Main game loop
        running = True
        while running:
            # Check if any UI elements are being hovered over
            submit_hover_active = button.collidepoint(pg.mouse.get_pos())
            live_true_hover_active = live_true_button.collidepoint(pg.mouse.get_pos())
            live_false_hover_active = live_false_button.collidepoint(pg.mouse.get_pos())
            reset_hover_active = reset_button.collidepoint(pg.mouse.get_pos())
            
            reset_hover_color = hover_active_color if reset_hover_active else hover_inactive_color
            submit_hover_color = hover_active_color if submit_hover_active else hover_inactive_color
            live_true_hover_color = hover_active_color if live_true_hover_active else hover_inactive_color
            live_false_hover_color = hover_active_color if live_false_hover_active else hover_inactive_color
            
            # Loop for handling all events
            for event in pg.event.get():
                # Handles moving the terminal
                self.handle_scroll_wheel(event)
                self.handle_drag_events(event)

                if event.type == pg.QUIT: # Close the application when the user exits
                    running = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    # Handle mouse click events for input fields and buttons
                    if button.collidepoint(event.pos):                                                                                                                                                                                                                                                                                         
                        live_value = 0 # Default live value (No)                    
                        if live_true_box_active:               
                            live_value = 1 # Set live value to Yes if the "YES" button is active
                        new_truck = Truck(
                            int(po_text),
                            int(size_text),
                            live_value,
                            self.env.now,
                            vendor_text.upper()
                        )
                        self.add_truck(self.env, new_truck)
                
                        
                    # Check which text input fields are clicked
                    if reset_button.collidepoint(event.pos):
                        po_text = ''
                        size_text = ''
                        vendor_text = ''
                        live_false_box_active = False
                        live_true_box_active = False

                        
                    # Sets or unsets all the text boxes if needed
                    if po_input_box.collidepoint(event.pos):
                        po_text_box_active = True
                    else:
                        po_text_box_active = False

                    if vendor_input_box.collidepoint(event.pos):
                        vendor_text_box_active = True
                    else:
                        vendor_text_box_active = False
                    
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
                    vendor_text_box_color = active_color if vendor_text_box_active else inactive_color
                    live_true_box_color = active_color if live_true_box_active else inactive_color
                    live_false_box_color = active_color if live_false_box_active else inactive_color
                
                if event.type == pg.KEYDOWN:
                    # Handle text input for each active text box
                    if po_text_box_active:
                        if event.key == pg.K_BACKSPACE:
                            backspace_active = True
                        else:
                            po_text += event.unicode
                    
                    if size_text_box_active:
                        if event.key == pg.K_BACKSPACE:
                            backspace_active = True

                        else:
                            size_text += event.unicode

                    if vendor_text_box_active:
                        if event.key == pg.K_BACKSPACE:
                            backspace_active = True

                        else:
                            vendor_text += event.unicode
                    
                else:
                    backspace_active = False
            
            # Handles deletion of text while backspace is being held
            if backspace_active:
                if po_text_box_active:
                    po_text = po_text[:-1]
                    
                if size_text_box_active:
                    size_text = size_text[:-1]

                if vendor_text_box_active:
                    vendor_text = vendor_text[:-1]

            # Update the display with the new graphical elements
            DISPLAYSURF.fill(GRAY)
            pg.draw.rect(DISPLAYSURF, GRAY, input_background)
            pg.draw.rect(DISPLAYSURF, submit_hover_color, button_outline)
            pg.draw.rect(DISPLAYSURF, reset_hover_color, reset_button_outline)
            pg.draw.rect(DISPLAYSURF, GRAY, reset_button_background)
            pg.draw.rect(DISPLAYSURF, GRAY, button_background)
            pg.draw.rect(DISPLAYSURF, live_true_hover_color, live_true_outline)
            pg.draw.rect(DISPLAYSURF, GRAY, live_true_background)
            pg.draw.rect(DISPLAYSURF, live_false_hover_color, live_false_outline)
            pg.draw.rect(DISPLAYSURF, GRAY, live_false_background)

            button_text_surface = font.render("Submit", True, BLACK)
            DISPLAYSURF.blit(button_text_surface, (button.x+5, button.y+10))
            pg.draw.rect(DISPLAYSURF, BLACK, button, 2)

            reset_button_text_surface = font.render("Reset", True, BLACK)
            DISPLAYSURF.blit(reset_button_text_surface, (reset_button.x+9, reset_button.y+10))
            pg.draw.rect(DISPLAYSURF, BLACK, reset_button, 2)

            po_text_surface = font.render(po_text, True, po_text_box_color)
            DISPLAYSURF.blit(po_text_surface, (po_input_box.x+5, po_input_box.y+5))
            pg.draw.rect(DISPLAYSURF, po_text_box_color, po_input_box, 2)

            po_label_surface = font.render('PO #:', True, WHITE)
            DISPLAYSURF.blit(po_label_surface, (po_label_box.x, po_label_box.y))

            size_text_surface = font.render(size_text, True, size_text_box_color)
            DISPLAYSURF.blit(size_text_surface, (size_input_box.x+5, size_input_box.y+5))
            pg.draw.rect(DISPLAYSURF, size_text_box_color, size_input_box, 2)
            
            vendor_label_surface = font.render("VENDOR:", True, WHITE)
            DISPLAYSURF.blit(vendor_label_surface, (vendor_label_box.x, vendor_label_box.y))

            vendor_text_surface = font.render(vendor_text, True, vendor_text_box_color)
            DISPLAYSURF.blit(vendor_text_surface, (vendor_input_box.x+5, vendor_input_box.y+5))
            pg.draw.rect(DISPLAYSURF, vendor_text_box_color, vendor_input_box, 2)

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

            # Draw all of the doors
            idx = 1
            for idx, door in enumerate(door_graphics):
                door_graphic = pg.Rect(DOOR_XPOSITION, DOOR_YPOSITION * (idx + 1), 40, 40)
                color = GREEN if door.unloading else RED
                door_visual = pg.draw.rect(DISPLAYSURF, color, door_graphic)
                door_text_surface = font.render('Door: ' + str(idx + 1), True, WHITE)
                self.mouse_hover_door(door_visual, DISPLAYSURF, door_text_surface)
                idx += 1
            
            # Draw all of the unloaders
            for unloader in self.unloader_graphics:
                unloader_text_surface = font.render('Unloader: ' + str(unloader.eid), True, WHITE)
                unloader_graphic = pg.draw.circle(DISPLAYSURF, BLACK, (unloader.x_position, unloader.y_position), 10)
                #DISPLAYSURF.blit(unloader_text_surface, (unloader.x_position - 5, unloader.y_position - 5))
                self.mouse_hover_door(unloader_graphic, DISPLAYSURF, unloader_text_surface)

            # Call all outside methods
            self.draw_trucks(self.truck_graphics, DISPLAYSURF, font)
            self.update_trucks(self.truck_graphics, DOOR_XPOSITION, DOOR_YPOSITION)
            self.update_unloaders(DOOR_XPOSITION, DOOR_YPOSITION)
            self.draw_terminal(DISPLAYSURF, terminal_background, font) 
            self.draw_scrollbar(DISPLAYSURF)           

            pg.display.flip()
            clock.tick(30)
        
        print("End time: " + str(self.env.now))
        if self.experimental:
            print("Number of times live loads waited longer than two hours: " + str (self.over_live_wait_time))


    
    def update_unloaders(self, DOOR_XPOSITION, DOOR_YPOSITION):
        """
        Updates the positions of unloaders in the simulation. If unloaders have not yet reached their assigned doors, 
        they will continue to move towards them.

        Parameters:
            DOOR_XPOSITION (int): The x-coordinate of the door.
            DOOR_YPOSITION (int): The y-coordinate of the door.

        Returns:
            None
        """
        for unloader_graphic in self.unloader_graphics:
            if unloader_graphic.current_door != -1:
                if not unloader_graphic.reached_door:
                    unloader_graphic.go_in(DOOR_XPOSITION, DOOR_YPOSITION * unloader_graphic.current_door)
            else:
                if unloader_graphic.initial_x != unloader_graphic.x_position or unloader_graphic.initial_y != unloader_graphic.y_position:
                    unloader_graphic.go_out()
                    unloader_graphic.reached_door = False


    def update_trucks(self, trucks, DOOR_XPOSITION, DOOR_YPOSITION):
        """
        Updates the positions of trucks in the simulation. If trucks have reached their assigned doors and are done 
        unloading, they will exit the simulation. Otherwise, they will continue moving towards the door.

        Parameters:
            trucks (list): List of trucks to be updated.
            DOOR_XPOSITION (int): The x-coordinate of the door.
            DOOR_YPOSITION (int): The y-coordinate of the door.

        Returns:
            None
        """
        for truck in trucks:
            if truck.gone:
                trucks.remove(truck)
            elif truck.reached_door and truck.done:
                truck.go_out()
            else:
                truck.go_in(DOOR_XPOSITION, DOOR_YPOSITION)

    def draw_trucks(self, trucks, surface, font):
        """
        Draws the trucks on the screen.

        Parameters:
            trucks (list): List of trucks to be drawn.
            surface (Surface): The Pygame surface on which the trucks will be rendered.
            font (Font): The Pygame font used to render truck PO numbers.

        Returns:
            None
        """
        for truck in trucks:
            truck_object = pg.Rect(truck.truck_x_position, truck.truck_y_position, 100, 25)
            truck_text_surface = font.render('PO #: ' + str(truck.po_num), True, BLACK)
            pg.draw.rect(surface, WHITE, truck_object)
            self.mouse_hover_truck(truck_object, surface, truck_text_surface)

    def add_text(self, new_text):
        """
        Adds a new line of text to the terminal log.

        Parameters:
            new_text (str): The text to be added to the terminal.

        Returns:
            None
        """
        self.lines.append(new_text)
        if len(self.lines) > 50:
            self.lines.pop(0)


    def draw_terminal(self, DISPLAYSURF, terminal_background, font):
        """
        Draws the terminal window and its text content to the screen. Implements scrolling when there is more text
        than can fit in the terminal window.

        Parameters:
            DISPLAYSURF (Surface): The Pygame surface on which the terminal will be rendered.
            terminal_background (Rect): The rectangle defining the area of the terminal.
            font (Font): The font used to render the terminal text.

        Returns:
            None
        """
        pg.draw.rect(DISPLAYSURF, BLACK, terminal_background)
        y_offset = terminal_background.y
        start_line = max(0, self.scroll_offset)
        end_line = min(start_line + self.max_lines, len(self.lines))
        
        for i in range(start_line, end_line):
             text_surface = font.render(self.lines[i], True, WHITE)  # Render text
             DISPLAYSURF.blit(text_surface, (0, y_offset))  # Draw text
             y_offset += self.FONT_SIZE  # Move text down

    
    def draw_scrollbar(self, DISPLAYSURF):
        """
        Draws the scrollbar on the screen. If there are more lines than can fit in the terminal, the scrollbar
        will appear and be scaled according to the number of lines.

        Parameters:
            DISPLAYSURF (Surface): The Pygame surface on which the scrollbar will be rendered.

        Returns:
            None
        """
        if len(self.lines) <= self.max_lines:
            return  # No scrollbar needed if all text fits

        scrollbar_x = 350 - self.SCROLLBAR_WIDTH  # Align to the right
        scrollbar_height = max(20, (self.max_lines / len(self.lines)) * self.TERMINAL_HEIGHT)  # Scale scrollbar
        scrollbar_y = self.TERMINAL_Y + (self.scroll_offset / (len(self.lines) - self.max_lines)) * (self.TERMINAL_HEIGHT - scrollbar_height) + (self.SCREEN_HEIGHT - self.TERMINAL_HEIGHT)
        pg.draw.rect(DISPLAYSURF, WHITE, (scrollbar_x, scrollbar_y, self.SCROLLBAR_WIDTH, scrollbar_height))

    
    def handle_scroll_wheel(self, event):
        """
        Handles mouse scroll wheel events to scroll the terminal up or down.

        Parameters:
            event (Event): The Pygame event triggered by mouse scrolling.

        Returns:
            None
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif event.button == 5:  # Scroll down
                self.scroll_offset = min(len(self.lines) - self.max_lines, self.scroll_offset + 1)

    def handle_drag_events(self, event):
        """
        Handles dragging on the scrollbar to change the scroll position.

        Parameters:
            event (Event): The Pygame event triggered by mouse dragging.

        Returns:
            None
        """

        scrollbar_rect = self.get_scrollbar_rect()
        max_scroll = max(1, len(self.lines) - self.max_lines)

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and scrollbar_rect and scrollbar_rect.collidepoint(event.pos):
                self.dragging = True
                self.drag_start_y = event.pos[1]
                self.initial_scroll_offset = self.scroll_offset

        elif event.type == pg.MOUSEMOTION:
            if self.dragging:
                dy = event.pos[1] - self.drag_start_y
                scroll_area_height = self.TERMINAL_HEIGHT - scrollbar_rect.height
                scroll_ratio = dy / scroll_area_height if scroll_area_height > 0 else 0
                self.scroll_offset = int(self.initial_scroll_offset + scroll_ratio * max_scroll)
                self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

    def get_scrollbar_rect(self):
        """
        Returns the rectangle representing the scrollbar based on the current scroll position.

        Returns:
            Rect: The rectangle for the scrollbar, or None if no scrollbar is needed.
        """
        if len(self.lines) <= self.max_lines:
            return None

        scrollbar_x = 350 - self.SCROLLBAR_WIDTH  # Align to the right
        scrollbar_height = max(20, (self.max_lines / len(self.lines)) * self.TERMINAL_HEIGHT)  # Scale scrollbar
        scrollbar_y = self.TERMINAL_Y + (self.scroll_offset / (len(self.lines) - self.max_lines)) * (self.TERMINAL_HEIGHT - scrollbar_height) + 320

        return pg.Rect(scrollbar_x, scrollbar_y, self.SCROLLBAR_WIDTH, scrollbar_height)

    def run_simulation(self):
        """
        Starts the simulation, printing the start time and running the simulation environment.

        Returns:
            None
        """
        print('The start time is: ' + str(self.env.now))
        self.env.run()

    
    def process_manager(self):
        """
        Manages the incoming trucks by checking for new processes and adding them to the simulation.

        Returns:
            None
        """
        #Constantly checks for new processes while keeping the simulation running
        while True:
            if self.incomingTrucks:
                nextTruck = self.incomingTrucks.pop(0)
                print(str(nextTruck.po) + " has arrived at " + str(nextTruck.time) + " size: " + str(nextTruck.size) + " env time: " + str(self.env.now))
                self.add_text(f"Truck number {nextTruck.po} is arriving at time {nextTruck.time}")
                self.trucks.addTruck(nextTruck, self.env)
                self.env.process(unloading(self))
            yield self.env.timeout(1)
    
    def add_truck(self, env, truck):
        """
        Adds a new truck to the incoming trucks list.

        Parameters:
            env (Environment): The simulation environment.
            truck (Truck): The truck to be added.

        Returns:
            None
        """
        self.incomingTrucks.append(truck)
    
    def add_truck_graphic(self, truck_graphic):
        """
        Adds a graphical representation of a truck to the list of truck graphics.

        Parameters:
            truck_graphic (TruckGraphic): The truck graphic to be added.

        Returns:
            None
        """
        self.truck_graphics.append(truck_graphic)
    
    def assign_unloader(self, unloader_graphic, door_num):
        """
        Assigns an unloader graphic to a specific door.

        Parameters:
            unloader_graphic (UnloaderGraphic): The unloader graphic to be assigned.
            door_num (int): The door number to assign the unloader to.

        Returns:
            None
        """
        unloader_graphic.current_door = door_num
    
    def mouse_hover_door(self, door, DISPLAYSURF, door_text_surface):
        """
        Checks if the mouse is hovering over a door

        Parameters:
            door (Door): The door to check if it is being hovered over.
            DISPLAYSURF (Surface): The current GUI to draw to.
            door_text_surface (Surface): the door surface to draw on

        Returns:
            None
        """
        pos = pg.mouse.get_pos()
        if door.collidepoint(pos):
            DISPLAYSURF.blit(door_text_surface, (pos[0] + 15, pos[1] + 15))

    def mouse_hover_unloader(self, unloader, DISPLAYSURF, unloader_text_surface):
        """
        Checks if the mouse is hovering over a unloader

        Parameters:
            unloader (Unloader): The unloader to check if it is being hovered over.
            DISPLAYSURF (Surface): The current GUI to draw to.
            door_text_surface (Surface): the door surface to draw on

        Returns:
            None
        """
        pos = pg.mouse.get_pos()
        if unloader.collidepoint(pos):
            DISPLAYSURF.blit(unloader_text_surface, (pos[0] + 15, pos[1] + 15))

    def mouse_hover_truck(self, truck, DISPLAYSURF, truck_text_surface):
        """
        Checks if the mouse is hovering over a truck

        Parameters:
            truck (Truck): The unloader to check if it is being hovered over.
            DISPLAYSURF (Surface): The current GUI to draw to.
            door_text_surface (Surface): the door surface to draw on

        Returns:
            None
        """
        pos = pg.mouse.get_pos()
        if truck.collidepoint(pos):
            DISPLAYSURF.blit(truck_text_surface, (pos[0] + 15, pos[1] + 15))

    # def warning_area(self, DISPLAYSURF, DOOR_XPOSITION, ):
    #     warning_area = pg.Rect(DOOR_XPOSITION, DOOR_YPOSITION * (idx + 1), 40, 40)

    
gui = GUI(experimental=True)
gui.animation()
pg.quit()
visualize()
