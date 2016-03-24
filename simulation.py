class Simulator(object):
    self.events = [] # queue of time  
    self.nodes = {}  # Key object
    self.numNodes = 100
    self.nodes = []
    self.numtasks = 10000

class Event(object):
    pass

class Node(object):
    self.id  = -1
    self.backups = {}  # (key, value) -> (Original Owner, [Keys])   
    self.shortPeers =  []
    self.longPeers = []
    
    
