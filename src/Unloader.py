from simpy import Resource

class Unloader(Resource):
    def __init__(self, env, eid, pph):
        Resource.__init__(self, env, capacity = 1)
        self.eid = eid
        self.pph = pph
