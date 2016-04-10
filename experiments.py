from simulation import Simulator
import variables
import statistics
import random

s = Simulator()
seed = 12345

def runTrials(strategy, homogeneity, workMeasurement, networkSize, jobSize, churn, adaptationRate, maxSybil, sybilThreshold, numSuccessors):
    global seed
    times = []
    inputs = "{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}".format(
        strategy, homogeneity, workMeasurement, networkSize, jobSize, churn, adaptationRate, maxSybil, sybilThreshold,numSuccessors, seed)
    with open("results.txt", 'a') as f:
            f.write(inputs)
            f.write("\n")
            f.write("____________________")
            f.write("\n")
    print(inputs)
    print("____________________")
    for _ in range(variables.trials):
        random.seed(seed)
        
        s.setupSimulation(strategy= strategy, homogeneity=homogeneity, workMeasurement= workMeasurement,numNodes=networkSize, 
            numTasks=jobSize, churnRate =churn, adaptationRate= adaptationRate, 
            maxSybil=maxSybil, sybilThreshold=sybilThreshold, numSuccessors=numSuccessors)
        
        loads = [len(x.tasks) for x in s.nodes.values()]  #this won't work once the network starts growing
        #print(sorted(loads))
        medianNumStartingTasks = statistics.median_low(loads)
        # variance
        # variance over time
        idealTime = s.perfectTime
        
        
        
        """
        x = s.nodeIDs
        y = [len(s.nodes[q].tasks) for q in s.nodeIDs]
        plt.plot(x,y, 'ro')
        plt.show()
        """
        numTicks, hardestWorker= s.simulate()
        
        slownessFactor  = numTicks/idealTime
        averageWorkPerTick = jobSize/numTicks
        results = "{:10}\t{:10}\t{:10}\t{:10}\t{:10}\t{:10}".format(
        numTicks, idealTime, slownessFactor, medianNumStartingTasks, averageWorkPerTick,  hardestWorker)
        with open("results.txt", 'a') as f:
            f.write(results)
            f.write("\n")
        print(results)
        times.append(numTicks)
        seed += 1
    ticks =  sum(times)/len(times)
    with open("averages.txt", 'a') as averages:
        averages.write(strategy + "\t"+ homogeneity  +"\t"+str(networkSize) + "\t" + str(jobSize) + "\t" + str(churn) + "\t"+ str(maxSybil) + "\t" + str(ticks) + str(seed-variables.trials)+"\n")
    #TODO graphs of graphs with sybil injections
    #print(str(networkSize) + "\t" + str(jobSize) + "\t" + str(churn) + "\t" + str(ticks))


def testPerStrength():
    for strategy in variables.strategies:
        for homogeneity in variables.homogeneity:
            runTrials(strategy, homogeneity, "perStrength", 1000, 100000, 0, 5, 5, 0.1, 5)
    
def testRandomInject():
    for homogeneity in variables.homogeneity:
        for workMeasurement in variables.workPerTick:
            for adaptationRate  in variables.adaptationRates:
                for maxSybil in variables.maxSybils:
                    for threshold in variables.sybilThresholds:
                        runTrials("randomInjection", homogeneity, workMeasurement, 1000, 100000, 0, adaptationRate, maxSybil, threshold, -1)

def testChurn():
    for churn in variables.churnRates:
        runTrials("churn", "equal", "one" ,  1000, 100000, churn, -1, -1, -1,-1)
            
#write a method to just check churn vs the random injection at 1000 100000 

def runFullExperiment():
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
                            """
                            I could swap theses out for continues at the bottom
                            """
                            if strategy == "randomInjection" or strategy == "neighbors":
                                rates = variables.adaptationRates
                                thresholds = variables.sybilThresholds
                                maxSybils = variables.maxSybils
                                if strategy == "neighbors":
                                    numSuccessorOptions = variables.successors
                            for adaptationRate in adaptationRates:
                                for maxSybil in maxSybils:
                                    for sybilThreshold in sybilThresholds:
                                        for numSuccessors in numSuccessorOptions:
                                            if strategy =="churn" and workMeasurement=="perSybil":
                                                continue
                                            runTrials(strategy, homogeneity, workMeasurement, networkSize, jobSize, churn, adaptationRate, maxSybil, sybilThreshold, numSuccessors)
                                            
                            
if __name__ == '__main__':
    print("Welcome to Andrew's Thesis Experiment. \n It's been a while.")
    print("Nodes \t\t Tasks \t\t Churn \t\t Time  \t\t Compare  \t\t medianStart \t\t avgWork \t\t mostWork")
    testPerStrength()
    #testChurn()
    #testRandomInject()