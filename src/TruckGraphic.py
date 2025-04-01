class TruckGraphic():
    def __init__(self, door_num, po_num):
        self.truck_x_position = 0
        self.truck_y_position = 0
        self.door_num = door_num
        self.po_num = po_num
        self.reached_door = False
        self.done = False
        self.gone = False
        
    
    def go_in(self, DOOR_XPOSITION, DOOR_YPOSITION):
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
        if self.truck_x_position > -100:
            self.truck_x_position -= 5
        else:
            self.gone = True
    