from simulation import Simulator
import variables
import statistics

s = Simulator()

def runTrials(strategy, homogeneity, networkSize, jobSize, churn, adaptationRate, maxSybil, sybilThreshold,numSuccessors):
    times = []
    inputs = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}".format(
        strategy, homogeneity, networkSize, jobSize, churn, adaptationRate, maxSybil, sybilThreshold,numSuccessors)
    with open("results.txt", 'a') as f:
            f.write(inputs)
            f.write("\n")
            f.write("____________________")
            f.write("\n")
    with open("averages.txt", 'a') as f:
            f.write(inputs)
            f.write("\n")
            f.write("____________________")
            f.write("\n")
    print(inputs)
    print("____________________")
    for _ in range(variables.trials):
        s.setupSimulation(strategy, homogeneity, numNodes=networkSize, 
            numTasks=jobSize, churnRate =churn, adaptationRate= adaptationRate, 
            maxSybil=maxSybil, sybilThreshold=sybilThreshold, numSuccessors=numSuccessors)
        
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
        slownessFactor  = numTicks/idealTime
        averageWorkPerTick = jobSize/numTicks
        results = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(
        numTicks, idealTime, slownessFactor, medianNumStartingTasks, averageWorkPerTick,  hardestWorker)
        with open("results.txt", 'a') as f:
            f.write(results)
            f.write("\n")
        print(results)
        times.append(numTicks)
    ticks =  sum(times)/len(times)
    with open("averages.txt", 'a') as averages:
        averages.write(strategy + "\t"+ homogeneity  +"\t"+str(networkSize) + "\t" + str(jobSize) + "\t" + str(churn) + "\t" + str(ticks) + "\n")
    #TODO graphs of graphs with sybil injections
    
    #print(str(networkSize) + "\t" + str(jobSize) + "\t" + str(churn) + "\t" + str(ticks))

def runRandomInject():
    for workMeasurement in variables.homogeneity:
        for adaptationRate  in variables.adaptationRates:
            for maxSybil in variables.maxSybils:
                for threshold in variables.sybilThresholds:
                    runTrials("randomInjection", workMeasurement, 1000, 100000, 0, adaptationRate, maxSybil, threshold, -1)

def testChurn():
    for churn in variables.churnRates:
        runTrials("churn", "equal", 1000, 100000, churn, -1, -1, -1,-1)
            
#write a method to just check churn vs the random injection at 1000 100000 

def runFullExperiment():
    for strategy in variables.strategies: 
        for workMeasurement in variables.homogeneity:
            for networkSize in variables.networkSizes:
                for jobSize in variables.jobSizes:
                    for churn in variables.churnRates:
                        adaptationRates = [-1]
                        sybilThresholds = [-1]
                        maxSybils = [-1]
                        numSuccessorOptions = [-1]
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
                                        runTrials(strategy, workMeasurement, networkSize, jobSize, churn, adaptationRate, maxSybil, sybilThreshold, numSuccessors)
                                        
                            
if __name__ == '__main__':
    print("Welcome to Andrew's Thesis Experiment. \n It's been a while.")
    print("Nodes \t\t Tasks \t\t Churn \t\t Time  \t\t Compare  \t\t medianStart \t\t avgWork \t\t mostWork")
    testChurn()