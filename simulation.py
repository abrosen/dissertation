import bisect
import builder


print("Begin")


class Simulator(object):
    events = [] # queue of timed events  
    nodeIDs = []
    nodes = {}  # (id: int, Node: object)
    
    
    numNodes = 1000
    numTasks = 1000000
    perfectTime = numTasks/numNodes
    numDone = 0
    time = 0 
    
    def whoGetsFile(self, key : int):
        i =  bisect.bisect_left(self.nodeIDs, key) # index of node closest without going over
        if i == len(self.nodeIDs):
            i = 0 
        return self.nodeIDs[i], i        
      
    
    def doTick(self):
        self.churnNetwork(self)
        self.performWork()
        self.time += 1    
    
    def churnNetwork(self):
        pass
    
    def performWork(self):
        for n in self.nodes:
            workDone = self.nodes[n].doWork()
            if workDone:  # if the node finished a task
                self.numDone += 1
    
    def simulate(self):
        while(self.numDone < self.numTasks):
            self.doTick()
            print(self.time, self.numDone)
        print(str(self.numTasks) + " done in " + str(self.time) + " ticks.")
        print(self.perfectTime)
        
        # maxNode =max(self.nodes.values(), key= lambda x: len(x.done))
        # print(len(maxNode.done))
    
    def __init__(self, topology =  "chord", strategy = "static"):
        self.nodeIDs = builder.createStaticIDs(self.numNodes)
        print("Creating Nodes")
        for id in self.nodeIDs:
            n = SimpleNode(id)
            self.nodes[id] = n
        print("Creating Tasks")
        for key in builder.generateFileIDs(self.numTasks):
            id, _ = self.whoGetsFile(key)
            self.nodes[id].addTask(key)


class SimpleNode(object):
    def __init__(self, id):
        self.id = id
        self.tasks = []
        self.done = []
    
    def doWork(self):
        if len(self.tasks) > 0:
            x = self.tasks.pop()
            self.done.append(x)
            return True
        return False
    
    def addTask(self,task):
        self.tasks.append(task)


class Task(object):
    def __init__(self, key, size=1):
        self.key = key
        self.size = size
        

class Result(object):
    results = []
    
    def combine(self, other) -> None:
        self.results = self.results + other.results


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


s = Simulator()
s.simulate()    