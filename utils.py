"""
Utilities for visualization
Ernesto Costa, February 2016
Adjusted by Sebastian Rehfeldt
"""

import matplotlib.pyplot as plt

# auxiliary 
def display(indiv, phenotype):
    print('Chromo: %s\nFitness: %s' % (phenotype(indiv[0]),indiv[1]))
    
def display_stat_1(best,average):
    generations = list(range(len(best)))
    plt.title('Performance over generations')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, best, label='Best')
    plt.plot(generations,average,label='Average')
    plt.legend(loc='best')
    plt.show()
    
def display_stat_n(boa,average_best):
    generations = list(range(len(boa)))
    plt.title('Performance over runs')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, boa, label='Best of All')
    plt.plot(generations,average_best,label='Average of Bests')
    plt.legend(loc='best')
    plt.show()
    
def readData(file):
    givens = {}

    with  open(file) as f:
        dimension = f.readline()
        data = f.readlines()
        i = 0
        for line in data:
            givens[i] = []
            elements = line.split()
            j=0
            for elem in elements:
                elem = int(elem)
                if not elem == 0:
                    givens[i].append((j,elem))
                j+=1

            i+=1
    
    f.closed
    return givens, int(dimension)