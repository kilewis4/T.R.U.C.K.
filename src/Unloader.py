from simpy import Resource

"""
Unloader class that defines an object that represents a loader.
"""
class Unloader(Resource):
    """
    Initializes an Unloader object.

    Args:
        env(Environment): enviorment to be passed when initializing 
        the resource
        eid(String): Employee identification number
        pph(int): Pallets per hour
    """
    def __init__(self, env, eid, pph, deviceName):
        Resource.__init__(self, env, capacity = 1)
        self.eid = eid
        self.pph = pph
        self.deviceName = deviceName
