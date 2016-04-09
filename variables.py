# integrated variables 
trials = 1
strategies = [ "churn", "randomInjection", "neighbors"]
homogeneity = ["equal", "strength", "sybil"]



networkSizes = [10, 50, 100, 500, 1000, 5000, 10000]
jobSizes = [100, 1000, 5000, 10000, 50000, 100000, 500000, 1000000, 10000000]
churnRates = [0, 0.00001, 0.0001, 0.001, 0.01]
adaptationRates = [1, 5, 10]
sybilThresholds = [0, 0.01, 0.1, 0.25] 

maxSybils = [1,5,10,50]
successors = [5,10,20]

# unintegrated variables








"""
outputs be sure to add average number of tasks done each tick

"""