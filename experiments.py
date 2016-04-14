from simulation import Simulator
import variables
import statistics
import random
import time

s = Simulator()
seed = 12345
start = str( int( time.time() ) )

def runTrials(strategy, homogeneity, workMeasurement, networkSize, jobSize, churn, adaptationRate, maxSybil, sybilThreshold, numSuccessors):
    global seed
    """
    if seed < 13745:
        seed += variables.trials
        return
    """
    times = []
    idealTimes = []
    medianLoads = []
    stdDevs = []
    workPerTickList = []
    hardestWorkers = []
    
    inputs = "{:<15} {:<15} {:<15} {:5d} {:8d} {:8.6f} {: 4d} {: 4d} {: 4.2f} {: 4d} {:6d}".format(
        strategy, homogeneity, workMeasurement, networkSize, jobSize, churn, adaptationRate, maxSybil, sybilThreshold,numSuccessors, seed)
    
    with open("data/results-" +start +  ".txt", 'a') as f:
            f.write(inputs)
            f.write("\n")
    print(inputs)
    
    for _ in range(variables.trials):
        
        random.seed(seed)
        
        s.setupSimulation(strategy= strategy, homogeneity=homogeneity, workMeasurement= workMeasurement,numNodes=networkSize, 
            numTasks=jobSize, churnRate =churn, adaptationRate= adaptationRate, 
            maxSybil=maxSybil, sybilThreshold=sybilThreshold, numSuccessors=numSuccessors)
        
        loads = [len(x.tasks) for x in s.nodes.values()]  #this won't work once the network starts growing
        #print(sorted(loads))
        medianNumStartingTasks = statistics.median_low(loads)
        medianLoads.append(medianNumStartingTasks)
        stdDevOfLoad = statistics.pstdev(loads)
        stdDevs.append(stdDevOfLoad)
        # variance
        # variance over time
        idealTime = s.perfectTime
        idealTimes.append(idealTime)
        
        
        """
        x = s.nodeIDs
        y = [len(s.nodes[q].tasks) for q in s.nodeIDs]
        plt.plot(x,y, 'ro')
        plt.show()
        """
        numTicks, hardestWorker= s.simulate()
        times.append(numTicks)
        hardestWorkers.append(hardestWorker)
        
        slownessFactor  = numTicks/idealTime
        averageWorkPerTick = jobSize/numTicks
        workPerTickList.append(averageWorkPerTick)
        
        results = "{:8d} {:8.3f} {:7.3f} {:6d} {:10.3f} {:10.3f} {:8d}".format(
        numTicks, idealTime, slownessFactor, medianNumStartingTasks, stdDevOfLoad, averageWorkPerTick,  hardestWorker)
        
        with open("data/results-"+start +".txt", 'a') as f:
            f.write(results)
            f.write("\n")
        print(results)
        
        seed += 1
    avgTicks =  sum(times)/len(times)
    avgIdealTime = sum(idealTimes)/len(idealTimes)
    avgSlowness = avgTicks/avgIdealTime
    
    avgMedianLoad = sum(medianLoads)/len(medianLoads)
    avgStdDev = sum(stdDevs)/len(stdDevs)
    
    avgAvgWorkPerTick = sum(workPerTickList)/len(workPerTickList)
    avgHardestWork  = sum(hardestWorkers)/len(hardestWorkers)
    
    outputs = "{:10.2f} {:8.3f} {:7.3f} {:10.3f} {:10.3f} {:10.2f} {:8.2f}".format(
        avgTicks, avgIdealTime, avgSlowness, avgMedianLoad, avgStdDev, avgAvgWorkPerTick, avgHardestWork)
    
    
    with open("data/averages-"+ start+".txt", 'a') as averages:
        averages.write(inputs + " " + outputs +"\n")
    #TODO graphs of graphs with sybil injections
    #print(str(networkSize) + "\t" + str(jobSize) + "\t" + str(churn) + "\t" + str(ticks))


def testPerStrength():
    for strategy in variables.strategies:
        for homogeneity in variables.homogeneity:
            runTrials(strategy, homogeneity, "perStrength", 1000, 100000, 0, 5, 5, 0.1, 5)

def testChurn():
    for churn in variables.churnRates:
        runTrials("churn", "equal", "one" ,  1000, 100000, churn, -1, -1, -1,-1)
     

    
def testRandomInject():
    for homogeneity in variables.homogeneity:
        for adaptationRate  in variables.adaptationRates:
            for maxSybil in variables.maxSybils:
                for threshold in variables.sybilThresholds:
                    runTrials("randomInjection", homogeneity, "one", 1000, 100000, 0, adaptationRate, maxSybil, threshold, -1)


def testNeighbor():
    for homogeneity in variables.homogeneity:
        for adaptationRate  in variables.adaptationRates:
            for maxSybil in variables.maxSybils:
                for threshold in variables.sybilThresholds:
                    for numSuccessor in variables.successors:
                        runTrials("neighbors", homogeneity, "one", 1000, 100000, 0, adaptationRate, maxSybil, threshold, numSuccessor)

def testInvite():
    for homogeneity in variables.homogeneity:
        for adaptationRate  in variables.adaptationRates:
            for maxSybil in variables.maxSybils:
                for threshold in variables.sybilThresholds:
                    for numSuccessor in variables.successors:
                        runTrials("invite", homogeneity, "one", 1000, 100000, 0, adaptationRate, maxSybil, threshold, numSuccessor)


def runMedianData():
    numExperiments = 0
    for networkSize in variables.networkSizes:
        for jobSize in variables.jobSizes:
            runTrials("churn", "equal", "one", networkSize, jobSize, 0, -1, -1, -1, -1)
            numExperiments +=1
    print(numExperiments*variables.trials)

def runChurn():
    numExperiments = 0
    for homogeneity in variables.homogeneity:
        for workMeasurement in variables.workPerTick:
            for networkSize in variables.networkSizes:
                for jobSize in variables.jobSizes:
                    for churn in variables.churnRates:
                        adaptationRates = [-1]
                        sybilThresholds = [-1]
                        maxSybils = [1]
                        numSuccessorOptions = [-1]
                        for adaptationRate in adaptationRates:
                            for maxSybil in maxSybils:
                                for sybilThreshold in sybilThresholds:
                                    for numSuccessors in numSuccessorOptions:
                                        if workMeasurement=="perSybil":
                                            continue
                                        runTrials("churn", homogeneity, workMeasurement, networkSize, jobSize, churn, adaptationRate, maxSybil, sybilThreshold, numSuccessors)
                                        numExperiments +=1
    print(numExperiments*variables.trials)


def runChurnLimitedSize(numNodes = 1000 , numtasks =100000):
    numExperiments = 0
    for homogeneity in variables.homogeneity:
        for workMeasurement in variables.workPerTick:
            for churn in variables.churnRates:
                adaptationRates = [-1]
                sybilThresholds = [-1]
                maxSybils = [1]
                numSuccessorOptions = [-1]
                for adaptationRate in adaptationRates:
                    for maxSybil in maxSybils:
                        for sybilThreshold in sybilThresholds:
                            for numSuccessors in numSuccessorOptions:
                                if workMeasurement=="perSybil":
                                    continue
                                runTrials("churn", homogeneity, workMeasurement, numNodes, numtasks, churn, adaptationRate, maxSybil, sybilThreshold, numSuccessors)
                                numExperiments +=1
    print(numExperiments*variables.trials)



def runRandomInjectLimitedSize(numNodes =1000, numTasks = 100000):
    numExperiments = 0
    for homogeneity in variables.homogeneity:
        for workMeasurement in variables.workPerTick:
            for churn in variables.churnRates:
                for adaptationRate in variables.adaptationRates:
                    for maxSybil in variables.maxSybils:
                        for sybilThreshold in variables.sybilThresholds:
                            #for numSuccessors in variables.successors:
                            if workMeasurement=="perSybil":
                                continue
                            runTrials("randomInjection", homogeneity, workMeasurement, numNodes, numTasks, churn, adaptationRate, maxSybil, sybilThreshold, -1)
                            numExperiments +=1
    print(numExperiments*variables.trials)
    
def runNeighborLimitedSize(numNodes =1000 , numTasks =100000):
    numExperiments = 0
    for homogeneity in variables.homogeneity:
        for workMeasurement in variables.workPerTick:
            for churn in variables.churnRates:
                for adaptationRate in variables.adaptationRates:
                    for maxSybil in variables.maxSybils:
                        for sybilThreshold in variables.sybilThresholds:
                            for numSuccessors in variables.successors:
                                if workMeasurement=="perSybil":
                                    continue
                                runTrials("neighbors", homogeneity, workMeasurement, numNodes, numTasks, churn, adaptationRate, maxSybil, sybilThreshold, numSuccessors)
                                numExperiments +=1
    print(numExperiments*variables.trials)
    
def runInviteLimitedSize(numNodes = 1000, numTasks= 100000):
    numExperiments = 0
    for homogeneity in variables.homogeneity:
        for workMeasurement in variables.workPerTick:
            for churn in variables.churnRates:
                for adaptationRate in variables.adaptationRates:
                    for maxSybil in variables.maxSybils:
                        for sybilThreshold in variables.sybilThresholds:
                            for numSuccessors in variables.successors:
                                if workMeasurement=="perSybil":
                                    continue
                                runTrials("invite", homogeneity, workMeasurement,numNodes, numTasks , churn, adaptationRate, maxSybil, sybilThreshold, numSuccessors)
                                numExperiments +=1
    print(numExperiments*variables.trials)



def runFullExperiment():
    numExperiments = 0
    for strategy in variables.strategies: 
        for homogeneity in variables.homogeneity:
            for workMeasurement in variables.workPerTick:
                for networkSize in variables.networkSizes:
                    for jobSize in variables.jobSizes:
                        for churn in variables.churnRates:
                            adaptationRates = [-1]
                            sybilThresholds = [-1]
                            maxSybils = [1]
                            numSuccessorOptions = [-1]
                            if strategy == "randomInjection" or strategy == "neighbors" or  strategy == "invite":
                                adaptationRates = variables.adaptationRates
                                sybilThresholds = variables.sybilThresholds
                                maxSybils = variables.maxSybils
                                if strategy == "neighbors" or strategy == "invite":
                                    numSuccessorOptions = variables.successors
                            for adaptationRate in adaptationRates:
                                for maxSybil in maxSybils:
                                    for sybilThreshold in sybilThresholds:
                                        for numSuccessors in numSuccessorOptions:
                                            if strategy =="churn" and workMeasurement=="perSybil":
                                                continue
                                            runTrials(strategy, homogeneity, workMeasurement, networkSize, jobSize, churn, adaptationRate, maxSybil, sybilThreshold, numSuccessors)
                                            numExperiments +=1
    print(numExperiments*variables.trials)
                            
if __name__ == '__main__':
    print("Welcome to Andrew's Thesis Experiment. \n It's been a while.")
    #print("Nodes \t\t Tasks \t\t Churn \t\t Time  \t\t Compare  \t\t medianStart \t\t avgWork \t\t mostWork")

    startTime = time.time()
    
    runInviteLimitedSize(20,2000)
    
    end= time.time()
    print("Time elapsed:" + str(end - startTime))
    
