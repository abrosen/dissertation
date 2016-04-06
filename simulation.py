import bisect
import builder
import random
import variables
import statistics
import matplotlib.pyplot as plt
import datetime
from variables import churnRates, adaptationRates


print("Begin")

maxSybils  = 10


class Simulator(object):
    def __init__(self):
        pass
       
    def setupSimulation(self, strategy= None, homogeneity= None, numNodes = 100, numTasks = 10000, churnRate = 0.01, adaptationRate = 5, maxSybil = 10, sybilThreshold = 0.1, numSuccessors=5):
        self.strategy = strategy
        
        self.nodeIDs = []   # the network topology
        self.superNodes = [] # the nodes that will do the sybilling  
        self.sybils = {} # (node, [] of sybils)
        self.pool = []
        self.nodes = {}  # (id: int, Node: object)
        
        
        self.numNodes = numNodes
        self.numTasks = numTasks
        self.churnRate = churnRate # chance of join/leave per tick per node
        self.adaptationRate = adaptationRate # number of ticks  
        self.maxSybil = maxSybil
        self.sybilThreshold = int((self.numTasks/self.numNodes) * sybilThreshold)
        self.numSuccessors = numSuccessors
        self.homogeneity = homogeneity
        
        self.perfectTime = self.numTasks/self.numNodes
        
        self.numDone = 0
        self.time = 0
        self.numSybils = 0
        
        #self.nodeIDs = builder.createStaticIDs(self.numNodes)
        for _ in range(self.numNodes):
            id = next(builder.generateFileIDs())
            self.nodeIDs.append(id)
            self.superNodes.append(id)
        self.addToPool(self.numNodes)
        
        self.nodeIDs = sorted(self.nodeIDs)
        self.superNodes = sorted(self.superNodes)
        
        #print("Creating Nodes")
        for id in self.superNodes:
            n = SimpleNode(id)
            self.nodes[id] = n
            
        #print("Creating Tasks")
        for key in [next(builder.generateFileIDs()) for _ in range(self.numTasks)]:
            id, _ = self.whoGetsFile(key)
            #print(id % 10000)
            self.nodes[id].addTask(key)
    
        
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
    
    def doTick(self):
        # assert(len(self.nodeIDs)  ==  len(set(self.nodeIDs)))
        if self.strategy == "randomInjection":
            self.randomInject()
        elif self.strategy == "neighbors":
            self.neighborInject()
        if not self.churnRate == 0:
            self.churnNetwork() #if churn is 0
        workThisTick = self.performWork()
        self.time += 1
        #print(self.time, self.numDone, workThisTick, len(self.superNodes), len(self.pool), len(self.nodeIDs) )
    
    
    def randomInject(self):
        if (self.time % self.adaptationRate) == 0:
            for nodeID in self.superNodes:
                node = self.nodes[nodeID]
                if (len(node.tasks) <= self.sybilThreshold) and self.canSybil(nodeID):  #what if threshhold is zero?
                    self.addSybil(nodeID)
                
                if nodeID in self.sybils and len(node.tasks) == 0:
                    self.clearSybils(nodeID)
    
    def neighborInject(self):
        if (self.time % self.adaptationRate) == 0:
            for nodeID in self.superNodes:
                node = self.nodes[nodeID]
                if len(node.tasks) <= self.sybilThreshold and self.canSybil(nodeID):
                    indexOfSybiler = self.nodeIDs.index(nodeID)
                    firstNeighbor = (indexOfSybiler + 1) % len(self.nodeIDs)
                    lastNeighbor = (indexOfSybiler + 1 + self.numSuccessors) % len(self.nodeIDs)
                    largestGap = 0 
                    boundaryA = -1 
                    boundaryB = -1
                    
                    for i, j in zip(range(indexOfSybiler, lastNeighbor - 1) , range(firstNeighbor, lastNeighbor)):
                        gapSize = (j - i) % builder.MAX
                        if gapSize >largestGap :
                            largestGap = gapSize
                            boundaryA = i
                            boundaryB = j
                    
                    # TODO Unsimplify.  Right now we just cheat and generate a number rather than hashing
                    a = (self.nodeIDs[boundaryA]+1) % builder.MAX 
                    b = (self.nodeIDs[boundaryB] -1) % builder.MAX
                    sybilID = self.mash(a, b)
                    self.addSybil(nodeID, sybilID)
                    #assert((a < sybilID and sybilID < b) or  ()  )
                    
                    
                    
    def mash(self, a:int, b :int) -> int:
        if b < a:
            offset = builder.MAX - a 
            b =  b + offset 
            a = 0
            retval  =  (random.randint(a, b) - offset)  % builder.MAX
            return retval
            
        return random.randint(a, b)
    
    def performWork(self):
        """
        equal = default = None: each supernode does one task, regardless of of num of sybils
        strength = each supernode does strength number of tasks
        sybil = node and sybil does one task per tick
        """
        workMeasurement = self.homogeneity
        numCompleted = 0
        population = None
        if workMeasurement is None or workMeasurement == "equal" or workMeasurement == 'default':
            population =  self.superNodes
        elif workMeasurement == 'strength' or workMeasurement == 'sybil':
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
    
    def canSybil(self, superNode):
        if superNode not in self.sybils.keys():
            return True
        return len(self.sybils[superNode]) < self.nodes[superNode].strength
    
    def addSybil(self, superNode, sybilID = None):
        if sybilID is None:
            sybilID =  next(builder.generateFileIDs())
        if superNode not in self.sybils:
            self.sybils[superNode] = [sybilID]
        else:
            self.sybils[superNode].append(sybilID)
        
        self.nodes[sybilID] = self.nodes[superNode]
        self.numSybils += 1
        self.insertWorker(sybilID, self.nodes[sybilID])
        
    def insertWorker(self, joiningID, node = None):
        index  = bisect.bisect_left(self.nodeIDs, joiningID)
        succ = None
        if index == len(self.nodeIDs): 
            succ =  self.nodes[self.nodeIDs[0]]
        else:
            succID = self.nodeIDs[index]
            succ =  self.nodes[succID]                
 
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
            self.numSybils -= 1
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
            self.clearSybils(key)
        return tasks
    
    def simulate(self):
        while(self.numDone < self.numTasks):
            self.doTick()
            
        #print(str(self.numTasks) + " done in " + str(self.time) + " ticks.")
        #print(self.perfectTime)
        maxNode =max(self.nodes.values(), key= lambda x: x.done)
        return self.time, maxNode.done
        # print(len(maxNode.done))
    
    

class SimpleNode(object):
    def __init__(self, id):
        self.id = id
        self.strength = maxSybils #random.randint(1, maxSybils )
        self.tasks = []
        self.done = 0
    
    def doWork(self):
        if len(self.tasks) > 0:
            x = self.tasks.pop()
            self.done += 1
            return True
        return False
    
    def addTask(self,task):
        self.tasks.append(task)




s = Simulator()
print("Nodes \t\t Tasks \t\t Churn \t\t Time  \t\t Compare  \t\t medianStart \t\t avgWork \t\t mostWork")

for networkSize in variables.networkSizes:
    for jobSize in variables.jobSizes:
        for churn in variables.churnRates:
            for strategy in variables.strategies:                   
                times = []
                for _ in range(variables.trials):
                    s.setupSimulation(strategy=strategy,numNodes=networkSize, numTasks=jobSize, churnRate =churn)
                    loads = [len(x.tasks) for x in s.nodes.values()]  #this won't work once the network starts growing
                    #print(sorted(loads))
                    medianNumStartingTasks = statistics.median_low(loads)
                    # variance
                    # variance over time
                    """
                    x = s.nodeIDs
                    y = [len(s.nodes[q].tasks) for q in s.nodeIDs]
                    plt.plot(x,y, 'ro')
                    plt.show()
                    """
                
                    numTicks, hardestWorker= s.simulate()
                    idealTime = jobSize/networkSize
                    slowness  = numTicks/idealTime
                    averageWorkPerTick = jobSize/numTicks
                    results = "{0}\t\t{1}\t\t{2}\t\t{3}\t\t{4}\t\t{5}\t\t{6}\t\t{7}".format(networkSize, jobSize, churn, numTicks, slowness,  medianNumStartingTasks, averageWorkPerTick,  hardestWorker)
                    with open("results.txt", 'a') as f:
                        f.write(results)
                        f.write("\n")
                    print(results)
                    times.append(numTicks)
                ticks =  sum(times)/len(times)
                with open("averages.txt", 'a') as averages:
                    averages.write(str(networkSize) + "\t" + str(jobSize) + "\t" + str(churn) + "\t" + str(ticks) + "\n")
                #print(str(networkSize) + "\t" + str(jobSize) + "\t" + str(churn) + "\t" + str(ticks))