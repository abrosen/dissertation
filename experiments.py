from simulation import Simulator
import variables
import statistics




def runTest():
    s = Simulator()
    print("Nodes \t\t Tasks \t\t Churn \t\t Time  \t\t Compare  \t\t medianStart \t\t avgWork \t\t mostWork")
    for strategy in variables.strategies: 
        for workMeasurement in variables.homogeneity:
            for networkSize in variables.networkSizes[4:5]:
                for jobSize in variables.jobSizes[5:6]:
                    for churn in variables.churnRates:
                        rates = []
                        if strategy == "churn":
                            rates = [1]
                        elif strategy == "randomInjection" or strategy == "neighbors":
                            rates = variables.adaptationRates
                        assert(rates != [])
                        for adaptationRate in rates:                    
                        
                            
                            
                            times = []
                            for _ in range(variables.trials):
                                s.setupSimulation(strategy=strategy,numNodes=networkSize, numTasks=jobSize, churnRate =churn, adaptationRate= adaptationRate)
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
                                results = "{0}\t\t{1}\t\t{2}\t\t{3}\t\t{4}\t\t{5}\t\t{6}\t\t{7}\t\t{8}".format(
                                networkSize, jobSize, churn,  numTicks,  slownessFactor, medianNumStartingTasks, averageWorkPerTick,  hardestWorker)
                                with open("results.txt", 'a') as f:
                                    f.write(results)
                                    f.write("\n")
                                print(results)
                                times.append(numTicks)
                            ticks =  sum(times)/len(times)
                            with open("averages.txt", 'a') as averages:
                                averages.write(strategy + "\t\t" +str(networkSize) + "\t\t" + str(jobSize) + "\t\t" + str(churn) + "\t\t" + str(ticks) + "\n")
                            #print(str(networkSize) + "\t" + str(jobSize) + "\t" + str(churn) + "\t" + str(ticks))
                        
if __name__ == '__main__':
    print("Welcome to Andrew's Thesis Experiment. \n It's been a while.")