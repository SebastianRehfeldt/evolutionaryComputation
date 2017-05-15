"""
sea_bin_visual.py
A very simple EA for binary representation.
Ernesto Costa
Adjusted by Sebastian Rehfeldt
"""


from random import random,randint, sample, seed, choice
from operator import itemgetter
from copy import deepcopy
import numpy as np

def run(numb_runs,numb_generations,size_pop, size_cromo, prob_mut, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_function, fix_func,givens):
    statistics = []
    for i in range(numb_runs):
        seed(i)
        best, stat_best, stat_aver = sea_for_plot(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_function, fix_func,givens)
        statistics.append(stat_best)
    stat_gener = list(zip(*statistics))
    best = [min(g_i) for g_i in stat_gener] # minimization
    aver_gener =  [sum(g_i)/len(g_i) for g_i in stat_gener]
    return best, aver_gener

# Return the best plus, best by generation, average population by generation
def sea_for_plot(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_function, fix_func, givens):
    # initialize population: indiv = (cromo,fit)
    population = gen_function(size_pop)
    population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]

    stat = [best_pop(population)[1]]
    stat_aver = [average_pop(population)]
    
    for i in range(numb_generations):
        old_pop = deepcopy(population)
        mate_pool = sel_parents(population)
        # Variation
        # ------ Crossover
        parents = []
        for j in  range(0,size_pop-1,2):
            cromo_1= mate_pool[j]
            cromo_2 = mate_pool[j+1]
            children = recombination(cromo_1,cromo_2, prob_cross)
            parents.extend(children) 
        # ------ Mutation
        descendents = []
        for indiv,fit in parents:
            new_indiv = mutation(indiv,prob_mut, givens)
            #mutation cant swap givens, so that there is no need to fix
            if prob_cross>0:
                new_indiv = fix_func(new_indiv)
            descendents.append((new_indiv,fitness_func(new_indiv)))
        # New population
        population = sel_survivors(old_pop,descendents)
        population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]
    
        # Estatistica
        stat.append(best_pop(population)[1])
        stat_aver.append(average_pop(population))
    
    return best_pop(population),stat, stat_aver


# Variation operators: Swap mutation for sub-blocks        
def swap_muta(indiv,prob_muta,givens):
    # Mutation by sub-blocks
    cromo = indiv[:]
    block=0
    d = int(np.sqrt(len(cromo)))
    for i in range(d):
        for j in range(d):
            
            value = random()            
            if value < prob_muta:
                row = i*d
                col = j*d
                elements = cromo[row:row+d,col:col+d].ravel()

                givs = givens[block]
                givens_pos = []
                for k in range(len(givs)):
                    pos = givs[k][0]
                    givens_pos.append(pos)

                rand1 = randint(0,8)
                while rand1 in givens_pos:
                    rand1 = randint(0,8)
                rand2 = randint(0,8)
                while rand2 in givens_pos or rand1 == rand2 :
                    rand2 = randint(0,8)

                elements[rand1],elements[rand2] = elements[rand2],elements[rand1]
                cromo[row:row+d,col:col+d] = np.reshape(elements,(-1,3))

            block += 1

    return cromo

# Variation Operators : Row swap crossover
def row_swap_cross(indiv_1, indiv_2,prob_cross):
    #swaps two rows between indivs
    value = random()
    if value < prob_cross:
        rand1 = randint(0,8)
        rand2 = randint(0,8)
        while rand1==rand2:
            rand2 = randint(0,8)

        temp = deepcopy(indiv_1[0][rand1,])
        indiv_1[0][rand1,] = indiv_2[0][rand2,]
        indiv_2[0][rand2,] = temp

        return (indiv_1,indiv_2)
    else:
        return (indiv_1,indiv_2)

#Block swap crossover
def block_swap_cross(indiv_1, indiv_2,prob_cross):
    #swaps two rows between indivs
    value = random()
    if value < prob_cross:
        rand1 = randint(0,8)
        rand2 = randint(0,8)
        while rand1==rand2:
            rand2 = randint(0,8)

        row1 = 3 * (int(rand1/3))
        col1 = 3 * (rand1%3)
        row2 = 3 * (int(rand2/3))
        col2 = 3 * (rand2%3)

        block1 = deepcopy(indiv_1[0][row1:row1+3,col1:col1+3])
        
        indiv_1[0][row1:row1+3,col1:col1+3] = indiv_2[0][row2:row2+3,col2:col2+3]
        indiv_2[0][row2:row2+3,col2:col2+3] = block1

        return (indiv_1,indiv_2)
    else:
        return (indiv_1,indiv_2)


# Parents Selection: tournament
def tour_sel(t_size):
    def tournament(pop):
        size_pop= len(pop)
        mate_pool = []
        for i in range(size_pop):
            winner = one_tour(pop,t_size)
            mate_pool.append(winner)
        return mate_pool
    return tournament

def one_tour(pop,size):
    """Minimization Problem. Deterministic"""
    pool = sample(pop, size)
    pool.sort(key=itemgetter(1), reverse=False)
    return pool[0]


# Survivals Selection: elitism
# minimization
def sel_survivors_elite(elite):
    def elitism(parents,offspring):
        size = len(parents)
        comp_elite = int(size* elite)
        offspring.sort(key=itemgetter(1), reverse=False)
        parents.sort(key=itemgetter(1), reverse=False)
        new_population = parents[:comp_elite] + offspring[:size - comp_elite]
        return new_population
    return elitism


# Auxiliary
# minimization
def best_pop(pop):
    pop.sort(key=itemgetter(1),reverse=False)

    return pop[0]

def average_pop(population):
    return sum([fit for cromo,fit in population])/len(population)