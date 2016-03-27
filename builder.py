from hashlib import sha1
import random

# Global constants
BASE = 160
MAX = 2**BASE

random.seed(12345)

def createStaticIDs(size):
    """
    This creates |size| IDs
    The output will be the same each time we run this. 
    """
    
    population = sorted([int(sha1(bytes(str( random.random()), "UTF-8")).hexdigest(), 16) 
                         % MAX for x in range(size)])
    return population


def generateFileIDs():
    # Create num random file ids
    while True:
        x = random.random()
        yield int(sha1(bytes(str(x), "UTF-8")).hexdigest(), 16) % MAX


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
        print("DONE")
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

