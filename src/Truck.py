"""
Truck class that contains the truck object constructor,
the incrementTime method, and __lt__ method.
"""
class Truck(object):
    """
    Constructor to create a truck object.

    Args:
        po(int): priority number of the truck, determines how
                 quickly an unloader will get around to it.
        size(int): size of the truck, determines how long it 
                   takes to unload
        live(int): Determines if the truck is a live load or not
        time(int): Determines the time of the truck's arrival.
    """
    def __init__(self, po, size, live, time, vendor):
        self.po = po
        self.size = size
        self.live = live
        self.time = time
        self.vendor = vendor

    """
    Increments the time of a truck by one, simulating the
    movement of time.
    """
    def incrementTime(self):
        self.time += 1

    """
    Checks if another truck's size and time of arrival is greater than its own.
    In the case of time, it checks if its greater than or equal to.

    Args:
        other(Truck): Another truck to be compared to.

    Returns:
        True or false based on if the current truck has a smaller size and
        earlier arrival time.
    """
    def __lt__(self, other):
        return self.size < other.size and self.time <= other.time
