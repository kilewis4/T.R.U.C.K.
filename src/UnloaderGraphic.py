import math
class UnloaderGraphic():
    def __init__(self, eid, x, y):
        self.current_door = -1
        self.initial_x = x
        self.initial_y = y
        self.x_position = x
        self.y_position = y
        self.eid = eid
        self.reached_door = False
        self.is_done = False
    
    def go_in(self, door_x, door_y):
        if self.x_position == door_x + 50 and self.y_position == door_y + 20:
            self.reached_door = True
        else:
            if self.y_position == door_y + 20:
                if self.x_position > door_x + 50:
                    self.x_position -= 5
            elif self.y_position > door_y + 20:
                self.y_position -= 5
            elif self.y_position < door_y + 20:
                self.y_position += 1
            

    def go_out(self):
        if self.x_position < self.initial_x:
                self.x_position += 5
        else:
            if self.y_position < self.initial_y - 5:
                self.y_position += 5
            elif self.y_position < self.initial_y:
                self.y_position += 1
            elif self.y_position > self.initial_y:
                self.y_position -= 1
        
        
        
    
