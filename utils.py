"""
Utilities for visualization
Ernesto Costa, February 2016
Adjusted by Sebastian Rehfeldt
"""

import matplotlib.pyplot as plt
import numpy as np

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
    
def display_stat_n(boa,average_best,i,prob_muta,cross_function):
    generations = list(range(len(boa)))
    plt.title('Performance over runs')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(generations, boa, label='Best of All')
    plt.plot(generations,average_best,label='Average of Bests')
    plt.legend(loc='best')
    plt.savefig('./experiments/file'+str(i)+'_'+cross_function+'_'+str(prob_muta)+'.png')
    plt.close()

    
def readData(file):
    # givens are saved in a dict
    # keys correspond to blocks
    # values are tuples containing a 1D position and a value

    givens = {}

    with  open(file) as f:
        dimension = int(f.readline())
        sudoku = np.zeros((dimension**2,dimension**2))

        data = f.readlines()
        i=0
        for line in data:
            elements = line.split()
            j=0
            for elem in elements:
                sudoku[i][j] = int(elem)
                j+=1
            i+=1

    block = 0
    for i in range(dimension):
            for j in range(dimension):
                row = i*dimension
                col = j*dimension
                elements = sudoku[row:row+dimension,col:col+dimension]
                elements = elements.ravel()
                givens[block] = []
                for k in range(len(elements)):
                    if not elements[k] == 0:
                        givens[block].append((k,int(elements[k])))
                block += 1

    f.closed
    return givens, dimension