"""

graph_bisection.py
Sebastian Rehfeldt

"""

from ea_sudoku_simple import *
from utils import *
import config

import os 


def fitness(givens):
    def fitness_(indiv):
        
        return evaluate(phenotype(indiv),givens)
    return fitness_

def phenotype(indiv):
    
    return []


def evaluate(pheno,graph):
    

    return []




if __name__ == '__main__':
    directory = os.getcwd()
    givens, dimension = readData(directory+"/cases/"+config.file)

    #indiv = [1,0,0,1]
    #pheno = phenotype(indiv)
    #print(pheno)

    cromo_size = dimension**2
    my_fitness = fitness(givens)

    n_runs = config.runs
    generations = config.generations
    pop_size = config.pop_size
    prob_muta = config.prob_muta
    prob_cross = config.prob_cross
    tour_size = config.tour_size
    elite_percent = config.elite_percent
    
    #print(my_fitness(indiv))

    #pass givens to ea or create initial pop here
    #best, stat, stat_average = sea_for_plot(generations, pop_size, cromo_size, prob_muta, prob_cross, tour_sel(tour_size), two_points_cross, muta_change, sel_survivors_elite(elite_percent), my_fitness)
    #display_stat_1(stat,stat_average)
    #print(best)
    

    #boa,stat_average = run(n_runs, generations, pop_size,cromo_size,prob_muta,prob_cross,tour_sel(tour_size),two_points_cross,muta_change,sel_survivors_elite(elite_percent), my_fitness)
    #display_stat_n(boa,stat_average)
    #print(min(boa))