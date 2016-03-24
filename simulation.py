class Simulator(object):
    events = [] # queue of timed events  
    nodes = {}  # Key object
    
    numNodes = 100
    nodes = []
    
    numtasks = 10000
    

class Event(object):
    pass

class Node(object):
    def __init__(self):
        self.id  = -1
        self.backups = {}  # (key, value) -> (Original Owner, [Keys])   
        self.shortPeers =  []
        self.longPeers = []
        self.files = {} # files[hashkey] = value , collisions overwrite (S.O.P.)
    
    def store(self,key , value):
        self.files[key] = value
        # do backup 