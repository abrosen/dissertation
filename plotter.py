import matplotlib.pyplot as plt
import math
import random
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
    plt.plot(fx,fy, 'bo')
    plt.show()

def drawAverageChurn(filename):
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
        plt.plot(result["rates"], result["times"], "-")
    plt.show()    

def drawRandomInjectionChurn(filename):
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
        plt.plot(result["rates"], result["times"], "-")
    plt.show()    


def plotLoads():
    s = Simulator()
    seed = 500
    loads = []
    for _ in range(10):
        random.seed(seed)
        s.setupSimulation(numNodes=1000,numTasks=100000)
        loads = loads + [len(x.tasks) for x in s.nodes.values()]
        seed += 1
    plt.hist(loads,200)
    plt.show()      

plotLoads()   
#drawAverageChurn("averagesChurn1k1m")