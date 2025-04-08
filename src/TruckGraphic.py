class TruckGraphic():
    """
    Represents a graphical representation of a truck in the simulation.

    Attributes:
        truck_x_position (int): The current x-position of the truck.
        truck_y_position (int): The current y-position of the truck.
        door_num (int): The door number that the truck is heading to.
        po_num (int): The purchase order number of the truck.
        reached_door (bool): Whether the truck has reached its destination door.
        done (bool): Whether the truck has completed its task.
        gone (bool): Whether the truck has left the area.
    """
    def __init__(self, door_num, po_num):
        """
        Initializes a new truck graphic object.

        Args:
            door_num (int): The door number that the truck will move towards.
            po_num (int): The purchase order number associated with the truck.
        """
        self.truck_x_position = 0
        self.truck_y_position = 0
        self.door_num = door_num
        self.po_num = po_num
        self.reached_door = False
        self.done = False
        self.gone = False
        
    
    def go_in(self, DOOR_XPOSITION, DOOR_YPOSITION):
        """
        Moves the truck towards the door, updating its position.

        Args:
            DOOR_XPOSITION (int): The x-position of the door.
            DOOR_YPOSITION (int): The y-position of the door.

        This method updates the truck's position as it moves towards the door
        by adjusting its `truck_x_position` and `truck_y_position`. Once the 
        truck reaches the target position, the `reached_door` flag is set to True.
        """
        if self.truck_x_position == DOOR_XPOSITION - 100 and self.truck_y_position == (DOOR_YPOSITION * self.door_num) + 5:
            self.reached_door = True
        else:
            if self.truck_x_position < DOOR_XPOSITION - 100:
                self.truck_x_position += 5
            if self.truck_x_position > DOOR_XPOSITION - 100:
                self.truck_x_position -= 1
            if self.truck_y_position > (DOOR_YPOSITION * self.door_num) + 5:
                self.truck_y_position -=1
            if self.truck_y_position < (DOOR_YPOSITION * self.door_num) + 5:
                self.truck_y_position += 5
    
    def go_out(self):
        """
        Moves the truck out of the area, decreasing its x-position.

        Once the truck's x-position goes beyond a certain threshold, the `gone`
        flag is set to True to indicate that the truck has left the area.
        """
        if self.truck_x_position > -100:
            self.truck_x_position -= 5
        else:
            self.gone = True
    