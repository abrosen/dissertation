import matplotlib.pyplot as plt
import math
import random
import statistics
from simulation import Simulator

from builder import generateFileIDs, MAX

def drawGraph(nodes, tasks):
    xs = []
    ys = [] 
    fx = []
    fy = []
    for _ in range(nodes):
        n = next(generateFileIDs())
        x = math.sin(2*math.pi*n/ MAX)
        y = math.cos(2*math.pi*n/ MAX)
        xs.append(x)
        ys.append(y)
    
    for _ in range(tasks):
        n = next(generateFileIDs())
        x = math.sin(2*math.pi*n/ MAX)
        y = math.cos(2*math.pi*n/ MAX)
        fx.append(x)
        fy.append(y)
    #plt.axes([-1.0,1.0,-1.0,1.0] )
    plt.plot(xs,ys, 'ro')
    plt.plot(fx,fy, 'b+')
    plt.show()

def drawAverageChurn(filename):
    data =  open("data/done/"+filename+".txt")
    results = []
    current = {}
    
    for line in data:
        line = line.split() 
        churnRate =  float(line[5])
        work =  float(line[-2])
        slownessFactor =  float(line[13])
        if churnRate == 0:
            current = {}
            current["homogeneity"] = line[1]
            current["workMeasurement"] = line[2]
            current["rates"] = []
            current["times"] = []
            current["work"] =  []
            results.append(current)
        current["rates"].append(churnRate)
        current["times"].append(slownessFactor)
        current["work"].append(work)
    for result in results:
        print(result["times"][0])
        plt.plot(result["rates"], result["times"], "o-")
        plt.xlabel("Churn Per Tick")
        plt.ylabel("Runtime") 
        plt.ylim(1,8)
        plt.xlim(0,0.1)  
        plt.show()    
        
        plt.plot(result["rates"], result["work"], "o-")
        plt.xlabel("Churn Per Tick")
        plt.ylabel("Avg Work Per Tick")
        plt.xlim(0,0.1)  
        plt.show()


def drawRandomInjection(filename):
    data =  open("data/done/"+filename+".txt")
    results = []
    current = {}
    
    for line in data:
        line = line.split() 
        churnRate =  float(line[5])
        slownessFactor =  float(line[13])
        if churnRate == 0:
            current = {}
            current["homogeneity"] = line[1]
            current["workMeasurement"] = line[2]
            current["rates"] = []
            current["times"] = []
            results.append(current)
        current["rates"].append(churnRate)
        current["times"].append(slownessFactor)
    for result in results:
        print(result["times"][0])
        plt.plot(result["rates"], result["times"], "o")
    plt.show()    

def testInjectionSteps():
    s =  Simulator()
    s.setupSimulation(strategy = 'randomInjections',workMeasurement="one", numNodes=1000, numTasks=100000)
    loads, medians, means, maxs, devs = s.simulateLoad()
    for i in range(0,len(loads), 5):
        x = loads[i]
        plt.hist(x, 100, normed =1 )
        plt.xlabel('Tasks Per Node')
        plt.ylabel('Probability')
        plt.axvline(medians[i], color='r', linestyle='--')
        plt.axvline(means[i], color='k', linestyle='--')
        #plt.ylim(0, 0.05)
        plt.show()


def compareChurnInjection():
    s =  Simulator()
    random.seed(125)
    s.setupSimulation(strategy= "churn",  workMeasurement= "one", numNodes= 1000, numTasks = 100000, churnRate =0.01)
    loads1, medians1, means1, maxs1, devs1 = s.simulateLoad()
    random.seed(125)
    s=Simulator()
    s.setupSimulation(strategy = 'randomInjections',workMeasurement="one", numNodes=1000, numTasks=100000, churnRate=0)    
    loads2 = s.simulateLoad()[0]
    for i in range(0,len(loads1), 5):
        x1= loads1[i]
        x2 =loads2[i]
        colors = ["blue", "red"]
        plt.hist([x1,x2], 100, normed =1, color=colors )
        plt.xlabel('Tasks Per Node')
        plt.ylabel('Probability')
        #plt.ylim(0, 0.05)
        plt.show()

def printTimeDiffs(fileA,fileB):
    naiveData = open("data/done/"+fileA+".txt")
    smartData = open("data/done/"+fileB+".txt") 
    diffs = []
    for line1, line2 in zip(naiveData, smartData):
        a = float(line1.split()[13])
        b = float(line2.split()[13])
        #print(a,b,a-b)
        diffs.append(a-b)
    print("A is this much slower than B:\t" + str(sum(diffs)/len(diffs)))

def plotLoads():
    s = Simulator()
    seed = 500
    loads = []
    for _ in range(20):
        random.seed(seed)
        s.setupSimulation(numNodes=1000,numTasks=1000000)
        loads = loads + [len(x.tasks) for x in s.nodes.values()]
        seed += 1
    n, bins, patches = plt.hist(loads, 150, normed =1 )
    plt.xlabel('Tasks Per Node')
    plt.ylabel('Probability')
    plt.axvline(statistics.median_low(loads), color='r', linestyle='--')
    plt.show()


drawGraph(10, 100)
#plotLoads()
#compareChurnInjection()
#drawAverageChurn("averagesChurnDataPoints")
#drawRandomInjection("averagesRandomInject1k1m")
#printTimeDiffs("averagesNeighbors1k100k", "averagesNeighborsSmart1k100k")
#printTimeDiffs("averagesChurn1k1m", "averagesChurn1h1m")
#printTimeDiffs("averagesChurn1k1m", "averagesChurn1k100k")
#printTimeDiffs("averagesRandomInjection1h10k", "averagesRandomInjection1k100k")
#printTimeDiffs("averagesRandomInjection1h100k", "averagesRandomInjection1k1m")
#printTimeDiffs("averagesRandomInjection1h10k", "averagesRandomInjection1h100k")
