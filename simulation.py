import bisect
import builder
import random
print("Begin")

maxSybils  = 10
class Simulator(object):
    def __init__(self, topology =  "chord", strategy = "static"):
        # Theses are defaults, setup new simulations with another func
        self.nodeIDs = []   # the network topology
        self.superNodes = [] # the nodes that will do the sybilling
        self.sybilIDs = []
        self.sybils = {} # (node, [] of sybils)
        self.pool = []
        self.nodes = {}  # (id: int, Node: object)
        
        
        self.numNodes = 100
        self.numTasks = 10000
        self.churnRate = 0.001 # chance of join/leave per tick per node
        self.adaptationRate = 5 # number of ticks  
        
        self.sybilThreshold = (self.numTasks/self.numNodes) / 10
        
        self.perfectTime = self.numTasks/self.numNodes
        
        self.numDone = 0
        self.time = 0
        
        #self.nodeIDs = builder.createStaticIDs(self.numNodes)
        for _ in range(self.numNodes):
            id = next(builder.generateFileIDs())
            self.nodeIDs.append(id)
            self.superNodes.append(id)
        self.addToPool(self.numNodes)
        
        print("Creating Nodes")
        for id in self.superNodes:
            n = SimpleNode(id)
            self.nodes[id] = n
            
        
        
        print("Creating Tasks")
        for key in [next(builder.generateFileIDs()) for _ in range(self.numTasks)]:
            id, _ = self.whoGetsFile(key)
            self.nodes[id].addTask(key)
        self.topology =  topology 
    
        
    def whoGetsFile(self, key : int):
        # returns closest node without going over and it's index in the nodeIDs
        i =  bisect.bisect_left(self.nodeIDs, key) # index of node closest without going over
        if i == len(self.nodeIDs):
            i = 0 
        return self.nodeIDs[i], i
     
    def reallocateTasks(self, tasks):
        for task in tasks:
            id, _  = self.whoGetsFile(task)
            self.nodes[id].addTask(task) 
    
    def doTick(self, workMeasurement =None):
        # assert(len(self.nodeIDs)  ==  len(set(self.nodeIDs)))
        self.randomInject()
        self.churnNetwork()
        workThisTick = self.performWork(workMeasurement)
        self.time += 1
        print(self.time, self.numDone, workThisTick, len(self.superNodes), len(self.pool), len(self.nodeIDs) )
    
    def randomInject(self):
        if (self.time % self.adaptationRate) == 0:
            for nodeID in self.superNodes:
                node = self.nodes[nodeID]
                if len(node.tasks) < self.sybilThreshold and self.canSybil(nodeID):
                    self.addSybil(nodeID)
                
                if nodeID in self.sybils and len(node.tasks) == 0:
                    self.clearSybils(nodeID)
    
    def performWork(self, workMeasurement = None):
        """
        equal = default = None: each supernode does one task, regardless of of num of sybils
        strength = each supernode does strength number of tasks
        sybil = node and sybil does one task per tick
        """
        
        numCompleted = 0
        population = None
        if workMeasurement is None or workMeasurement == "equal" or workMeasurement == 'default':
            population =  self.superNodes
        elif workMeasurement == 'sybil':
            population = self.nodeIDs
        
        for n in population:
            workDone = self.nodes[n].doWork()
            if workDone:  # if the node finished a task
                self.numDone += 1
                numCompleted += 1
        return numCompleted
        
        #for n in self.sybilIDs:
        #    workDone = self.nodes[n].doWork()
        #    if workDone:  # if the node finished a task
        #        self.numDone += 1
        
        
    def churnNetwork(self):
        """
        figure out who is leaving and store it
        figure out who is joining and store it
        for each leaving node,
            remove it
            collect tasks
        reassign tasks
        
        for each joining
            add new node
            reassign tasks from affected nodes
            
        generate new ids and add them to pool
        
        """
        leaving = []
        joining = []
        for nodeID in self.superNodes:
            if random.random() < self.churnRate:
                leaving.append(nodeID)
        for j in self.pool:
            if random.random() < self.churnRate:
                joining.append(j)
                self.pool.remove(j)
        
        tasks = []
        
        for l in leaving:
            tasks += self.removeNode(l)
        self.reallocateTasks(tasks)
        
        for j in joining:
            # assert(len(self.nodeIDs)  ==  len(set(self.nodeIDs)))
            self.insertWorker(j)
        self.addToPool(len(leaving))
    
    """    
    def numSybils(self, id):
        # number of sybils id has made.
        if id not in self.sybils.keys():
            return 0
        return len(self.sybils[id])
    """
    
    
    def canSybil(self, superNode):
        if superNode not in self.sybils.keys():
            return True
        return len(self.sybils[superNode]) < self.nodes[superNode].strength
    
    def addSybil(self, superNode):
        sybilID =  next(builder.generateFileIDs())
        if superNode not in self.sybils:
            self.sybils[superNode] = [sybilID]
        else:
            self.sybils[superNode].append(sybilID)
        
        self.nodes[sybilID] = self.nodes[superNode]
        self.sybilIDs.append(sybilID)
        
        # change this to grab the work
        self.insertWorker(sybilID, self.nodes[sybilID])
        
        
        
        #bisect.insort(self.nodeIDs, sybilID)
        
    def insertWorker(self, joiningID, node = None):
        index  = bisect.bisect_left(self.nodeIDs, joiningID)
        succ = None
        if index == len(self.nodeIDs): 
            succ =  self.nodes[self.nodeIDs[0]]
        else:
            succID = self.nodeIDs[index]
            succ =  self.nodes[succID]                
        # if j in self.nodeIDs:
        #    continue
        
        # assert(j not in self.nodeIDs)
        
        self.nodeIDs.insert(index, joiningID)         
        if node is None:
            node = SimpleNode(joiningID)
            self.nodes[joiningID] = node
            bisect.insort(self.superNodes, joiningID)
        
        tasks = succ.tasks[:]
        succ.tasks = []
        
        for task in tasks:
            if node.id < succ.id:
                if task <= node.id:
                    node.addTask(task)
                else:
                    succ.addTask(task)
            else:
                if task > succ.id and  task < node.id:
                    node.addTask(task)
                else:
                    succ.addTask(task)
 
    def clearSybils(self, superNode):
        for s in self.sybils[superNode]:
            del(self.nodes[s])
            self.sybilIDs.remove(s)
            self.nodeIDs.remove(s)
        self.sybils[superNode] = []
    
    def addToPool(self, num):
        # Adds num nodes to the pool of possible joining nodes
        for _ in range(num):
            x = next(builder.generateFileIDs())
            assert(x not in self.nodeIDs)
            self.pool.append(x)

    def removeNode(self, key):
        # kills a node with the id key
        tasks = self.nodes[key].tasks[:]
        self.superNodes.remove(key)
        self.nodeIDs.remove(key)
        del(self.nodes[key])
        
        # remove all sybils
        if key in self.sybils:
            for s in self.sybils[key]:
                del(self.nodes[s])
                self.sybilIDs.remove(s)
                self.nodeIDs.remove(s)
            del(self.sybils[key])
        return tasks
    
    
    
        
    
    
    def simulate(self,  workMeasurement = None):
        while(self.numDone < self.numTasks):
            self.doTick(workMeasurement)
            
        print(str(self.numTasks) + " done in " + str(self.time) + " ticks.")
        print(self.perfectTime)
        
        # maxNode =max(self.nodes.values(), key= lambda x: len(x.done))
        # print(len(maxNode.done))
    
    

class SimpleNode(object):
    def __init__(self, id):
        self.id = id
        self.strength = maxSybils #random.randint(1, maxSybils )
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



s = Simulator()
s.simulate()    
