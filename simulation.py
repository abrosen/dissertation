from hashlib import sha1
BASE = 160
MAX = 2**BASE

print("Begin")


def createStaticIDs(size):
    """
    This creates |size| IDs
    The output will be the same each time we run this. 
    """
    
    population = sorted([int(sha1(bytes(str(x), "UTF-8")).hexdigest(), 16) % MAX for x in range(size)])
    return population

print(createStaticIDs(10))


class Simulator(object):
    events = [] # queue of timed events  
    nodes = {}  # (id: int, Node: object)
    
    numNodes = 100
    numtasks = 10000   
    
    
    def doTick(self):
        for n in self.nodes:
            self.nodes[n].doWork()
    
    def __init__(self, topology, strategy):
        pass
    


    
    
class Event(object):
    pass

class Task(object):
    def __init__(self, key, size=1):
        self.key = key
        self.size = size
        

class Result(object):
    results = []
    
    def combine(self, other) -> None:
        self.results = self.results + other.results


class SimpleNode(object):
    def __init__(self, id):
        self.id = id
        self.tasks = []
    
    
    def doWork(self):
        pass








class DHTNode(object):
    def __init__(self,hashkey: int):
        self.id  = hashkey  # hashkey int from SHA1
        self.files = {}     # files[hashkey] = value , collisions overwrite (S.O.P.)
        self.backups = {}   # Original Owner -> {files})
                            # or should it just be like files
                            # or above + add another mapping  
        
        self.shortPeers =  []
        self.longPeers = [] # assumptions: lazy update for long peers to start 
                            # (eg find new one only when an error occurs)
                            # unless protocol specifies otherwise
        
        self.tasks = []
        self.backTask = {}  # Tasks that other nodes have been assigned.
        
        
        
        
    def store(self, key: int, value: int):
        self.files[key] = value
        # do backup 
        
    def backup(self, key: int, value:int)-> None:
        self.backups[key] = [value]
        
    def becomeOwner(self, key:int):
        self.files
        del self.backups[key]
    
    def relinquishOwnership(self, key:int):
        pass
    
print("DONE")