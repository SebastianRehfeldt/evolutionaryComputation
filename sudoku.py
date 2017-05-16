"""
sudoku.py
Sebastian Rehfeldt

"""

from ea_sudoku_simple import *
from utils import *
from collections import Counter

import config
import os
import numpy as np


# Initialize population
def gera_pop(dimension,fix_func):
    def _gera_pop(size_pop):
        return [(gera_indiv(dimension,fix_func),0) for i in range(size_pop)]
    return _gera_pop

def gera_indiv(dim,fix_func):
    # fill blocks with random permutation and fix givens later

    indiv = np.zeros((dim,dim))
    d = int(np.sqrt(dim))

    for i in range(d):
            for j in range(d):
                perm = np.random.permutation(9)+1
                row = i*d
                col = j*d

                indiv[row:row+d,col:col+d] = np.reshape(perm,(-1,3))
    
    indiv = fix_func(indiv)

    return indiv

def fix_givens(givens,dim):
    cross_func = config.cross_over
    def _fix_givens(indiv):
        d = int(np.sqrt(dim))
        #for each block fix the givens
        block = 0
        for i in range(d):
            for j in range(d):
                row = i*d
                col = j*d
                elements = indiv[row:row+d,col:col+d]
                elements = elements.ravel()
                givs = givens[block]
                givens_indices = []
                for k in range(len(givs)):
                    pos = givs[k][0]
                    givens_indices.append(pos)
                    val = givs[k][1]
                    if not int(elements[pos]) == val:
                        #swap each given to its correct position
                        if val in elements:
                            giv_pos = np.where(elements==val)[0][0]
                            elements[pos], elements[giv_pos] = val, int(elements[pos])
                        else:
                            elements[pos] = val

                if cross_func == "row":
                    while not len(set(elements)) == 9:
                        #remove duplicates

                        used = set(elements)
                        missing = list(set(np.random.permutation(9)+1)-used)
                        duplicates = list((Counter(elements) - Counter(set(elements))).keys())

                        # find indices for duplicated values
                        # set first non-given duplicated value to first missing value
                        dup = int(duplicates[0])
                        dup_pos = np.where(elements==dup)[0]
                        i = 0
                        while dup_pos[i] in givens_indices:
                            i+=1
                        elements[dup_pos[i]] = missing[0]


                indiv[row:row+d,col:col+d] = np.reshape(elements,(-1,3))
                block +=1

        return indiv
    return _fix_givens

def fitness(dimension):
    def fitness_(indiv):
        return evaluate(phenotype(indiv),dimension)
    return fitness_

def phenotype(indiv):
    #should be the same as the genotype
    return indiv


def evaluate(pheno,dimension):
    conflicts = 0

    #There are no conflicts inside the sub-boxes as the algorithm is implemented to keep this constraint
    conflicts += calculateRowConflicts(pheno,dimension)
    conflicts += calculateColumnConflicts(pheno,dimension)
    #conflicts += calculateDiagonalConflicts(pheno,dimension)

    return conflicts

def calculateRowConflicts(pheno,dimension):
    conflicts = 0
    for i in range(dimension):
        conflicts += dimension-len(set(pheno[i]))
    return conflicts

def calculateColumnConflicts(pheno,dimension):
    conflicts = 0
    for i in range(dimension):
        conflicts += dimension-len(set(pheno[:,i]))
    return conflicts


def calculateDiagonalConflicts(pheno,dimension):
    conflicts = 0
    diagonal1 = []
    diagonal2 = []
    for i in range(dimension):
        diagonal1.append(pheno[i,i])
        diagonal2.append(pheno[dimension-i-1,i])
    conflicts += dimension-len(set(diagonal1))
    conflicts += dimension-len(set(diagonal2))
    return conflicts



if __name__ == '__main__':
    
    # GET CONFIG
    n_runs = config.runs
    generations = config.generations
    pop_size = config.pop_size
    prob_muta = config.prob_muta
    prob_cross = config.prob_cross
    tour_size = config.tour_size
    elite_percent = config.elite_percent
    
    if config.cross_over == "block":
        cross_function = block_swap_cross
    else:
        cross_function = row_swap_cross

    # FOR EACH FILE
    directory = os.getcwd()
    files = config.test_files

    best_solutions = []
    aver_solutions = []
    best_generations = []
    aver_generations = []
    numb_solutions = []

    for i in range(len(files)):
        file = files[i]
        givens, dimension = readData(directory+"/cases/"+file)

    
        cromo_size = dimension**3 #total number of elements
        dimension = dimension**2 #dimension of genotype array

        fix_func = fix_givens(givens,dimension)
        gen_function = gera_pop(dimension, fix_func)
        my_fitness = fitness(dimension)

        #best, stat, stat_average = sea_for_plot(generations, pop_size, cromo_size, prob_muta, prob_cross, tour_sel(tour_size), cross_function, swap_muta, sel_survivors_elite(elite_percent), my_fitness, gen_function, fix_func, givens)
        #display_stat_1(stat,stat_average)
        #print(best)

        best,stat_average,final_conflicts,best_generation,aver_generation,numb_solution = run(n_runs, generations, pop_size,cromo_size,prob_muta,prob_cross,tour_sel(tour_size),cross_function,swap_muta,sel_survivors_elite(elite_percent), my_fitness, gen_function, fix_func, givens)
        display_stat_n(best,stat_average,i)

        # collect for printing to files
        best_solutions.append(min(final_conflicts))   
        aver_solutions.append(np.mean(final_conflicts))
        best_generations.append(best_generation)
        aver_generations.append(aver_generation)
        numb_solutions.append(numb_solution)

    # print results to files
    f = open('./experiments/final_conflicts.csv', 'w')
    f.write('file,best,average\n')
    for i in range(len(best_solutions)):
        f.write(str(i+1)+","+str(best_solutions[i])+","+str(aver_solutions[i])+"\n")
    f.close()

    f2 = open('./experiments/generations.csv', 'w')
    f2.write('file,best_generation,average_generation,found_solutions\n')
    for i in range(len(best_generations)):
        f2.write(str(i+1)+","+str(best_generations[i])+","+str(aver_generations[i])+","+str(numb_solutions[i])+"\n")
    f2.close()