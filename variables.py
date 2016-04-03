# integrated variables 
trials = 50
networkSizes = [10, 50, 100, 500, 1000, 2500, 5000, 10000]

# unintegrated variables

jobSizes = [100, 1000, 5000, 10000, 50000, 100000, 500000, 1000000, 10000000]
churnRates = [0, 0.00001, 0.0001, 0.001, 0.01]
adaptationRates = [1, 5, 10]
sybilThresholds = [0, 0.01, 0.1, 0.25] 
maxSybils = [1,5,10,50]

strategies = ["base", "random", "randomInjection", "neighbors"]
homogeneity = ["equal", "strength", "sybil"]


"""
outputs be sure to add average number of tasks done each tick

"""