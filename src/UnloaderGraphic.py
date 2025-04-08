import math

class UnloaderGraphic:
    """
    A class that represents the graphical representation of an unloader in a simulation.
    The unloader moves towards a specified door position and can return to its initial position.

    Attributes:
        current_door (int): The door the unloader is currently assigned to. Default is -1 (no door).
        initial_x (int): The initial x-coordinate of the unloader's starting position.
        initial_y (int): The initial y-coordinate of the unloader's starting position.
        x_position (int): The current x-coordinate of the unloader.
        y_position (int): The current y-coordinate of the unloader.
        eid (int): The unique identifier for the unloader.
        reached_door (bool): Flag indicating whether the unloader has reached the assigned door.
        is_done (bool): Flag indicating whether the unloader is done with its task.
    
    Methods:
        go_in(door_x, door_y): Moves the unloader towards the door's position.
        go_out(): Moves the unloader back to its initial position.
    """
    
    def __init__(self, eid, x, y):
        """
        Initializes the UnloaderGraphic with the specified ID and initial position.

        Args:
            eid (int): The unique identifier for the unloader.
            x (int): The initial x-coordinate of the unloader.
            y (int): The initial y-coordinate of the unloader.
        """
        self.current_door = -1  # Initially no door assigned
        self.initial_x = x
        self.initial_y = y
        self.x_position = x
        self.y_position = y
        self.eid = eid
        self.reached_door = False
        self.is_done = False

    def go_in(self, door_x, door_y):
        """
        Moves the unloader towards the specified door's coordinates (door_x, door_y).
        The unloader adjusts its position step by step until it reaches the door.

        Args:
            door_x (int): The x-coordinate of the door.
            door_y (int): The y-coordinate of the door.
        """
        # Check if the unloader has reached the door
        if self.x_position == door_x + 50 and self.y_position == door_y + 20:
            self.reached_door = True  # Mark as reached the door
        else:
            # Move unloader to the right if it's not at the correct x position
            if self.y_position == door_y + 20:
                if self.x_position > door_x + 50:
                    self.x_position -= 5  # Move left
            # Adjust the y-coordinate to match the door's y position
            elif self.y_position > door_y + 20:
                self.y_position -= 5  # Move up
            elif self.y_position < door_y + 20:
                self.y_position += 1  # Move down

    def go_out(self):
        """
        Moves the unloader back to its initial position. The unloader first moves horizontally
        and then vertically, depending on its current position.

        This method brings the unloader back to its original coordinates.
        """
        if self.x_position < self.initial_x:
            self.x_position += 5  # Move right if the unloader has not reached the initial x position
        else:
            # Adjust the y-coordinate to move back to the initial y position
            if self.y_position < self.initial_y - 5:
                self.y_position += 5  # Move down if too high
            elif self.y_position < self.initial_y:
                self.y_position += 1  # Fine-tune the y position to match initial y
            elif self.y_position > self.initial_y:
                self.y_position -= 1  # Move up if too low
