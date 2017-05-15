"""
sea_bin_visual.py
A very simple EA for binary representation.
Ernesto Costa
Adjusted by Sebastian Rehfeldt
"""


from random import random,randint, sample, seed, choice
from operator import itemgetter

def run(numb_runs,numb_generations,size_pop, size_cromo, prob_mut, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_function, fix_func):
    statistics = []
    for i in range(numb_runs):
        seed(i)
        best, stat_best, stat_aver = sea_for_plot(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_function, fix_func)
        statistics.append(stat_best)
    stat_gener = list(zip(*statistics))
    best = [min(g_i) for g_i in stat_gener] # minimization
    aver_gener =  [sum(g_i)/len(g_i) for g_i in stat_gener]
    return best, aver_gener

# Simple [Binary] Evolutionary Algorithm		
def sea(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_function, fix_func):
    # initialize population: indiv = (cromo,fit)
    population = gen_function(size_pop)
    # evaluate population
    population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]
    for i in range(numb_generations):
        # parents selection
        mate_pool = sel_parents(population)
	# Variation
	# ------ Crossover
        parents = []
        for i in  range(0,size_pop-1,2):
            indiv_1= mate_pool[i]
            indiv_2 = mate_pool[i+1]
            children = recombination(indiv_1,indiv_2, prob_cross)
            parents.extend(children) 
        # ------ Mutation
        descendentes = []
        for indiv,fit in parents:
            novo_indiv = mutation(indiv,prob_mut)
            descendentes.append((novo_indiv,fitness_func(novo_indiv)))
        # New population
        population = sel_survivors(population,descendentes)
        # Evaluate the new population
        population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]     
    return best_pop(population)


# Simple [Binary] Evolutionary Algorithm 
# Return the best plus, best by generation, average population by generation
def sea_for_plot(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func, gen_function, fix_func):
    # inicializa population: indiv = (cromo,fit)
    population = gen_function(size_pop)
    #print([sum(indiv[0]) for indiv in population])
    # avalia population
    population = [(indiv[0], fitness_func(indiv[0])) for indiv in population]

    # para a estatistica
    stat = [best_pop(population)[1]]
    stat_aver = [average_pop(population)]
    
    for i in range(numb_generations):
        # selecciona parents
        mate_pool = sel_parents(population)
    # Variation
    # ------ Crossover
        parents = []
        for i in  range(0,size_pop-1,2):
            cromo_1= mate_pool[i]
            cromo_2 = mate_pool[i+1]
            children = recombination(cromo_1,cromo_2, prob_cross)
            parents.extend(children) 
        # ------ Mutation
        descendentes = []
        for indiv,fit in parents:
            novo_indiv = mutation(indiv,prob_mut)
            descendentes.append((novo_indiv,fitness_func(novo_indiv)))
        # New population
        population = sel_survivors(population,descendentes)
        # Avalia nova _population
        population = [(indiv[0], fitness_func(indiv[0])) for indiv in population] 
    
    # Estatistica
        stat.append(best_pop(population)[1])
        stat_aver.append(average_pop(population))
    
    return best_pop(population),stat, stat_aver


# Variation operators: Binary mutation	    
def muta_change(indiv,prob_muta):
    # Mutation by gene
    cromo = indiv[:]

    orig_sum = sum(cromo)
    for i in range(len(indiv)):
        #change sets of cities (if one city is changed, a random city of the other set is also changed)
        cromo = muta_change_gene(cromo,i,prob_muta)

    new_sum = sum(cromo)

    if not orig_sum == new_sum:
        print(cromo)
        print(1/0)

    return cromo

def muta_change_gene(chromo, index, prob_muta):
    value = random()
    originalSet = chromo[index]

    if value < prob_muta:
        #flip random bit of other set
        if originalSet == 0:
            #flip a random 1
            indices = [i for i in range(len(chromo)) if chromo[i] == 1]
            chromo[choice(indices)] = 0
        else:
            #flip a random 0
            indices = [i for i in range(len(chromo)) if chromo[i] == 0]
            chromo[choice(indices)] = 1

        #flip bit
        chromo[index] ^= 1
    return chromo

# Variation Operators :Crossover
def one_point_cross(indiv_1, indiv_2,prob_cross):
	value = random()
	if value < prob_cross:
	    cromo_1 = indiv_1[0]
	    cromo_2 = indiv_2[0]
	    pos = randint(0,len(cromo_1))
	    f1 = cromo_1[0:pos] + cromo_2[pos:]
	    f2 = cromo_2[0:pos] + cromo_1[pos:]
	    return ((f1,0),(f2,0))
	else:
	    return (indiv_1,indiv_2)
	    
def two_points_cross(indiv_1, indiv_2,prob_cross):
	value = random()
	if value < prob_cross:
	    cromo_1 = indiv_1[0]
	    cromo_2 = indiv_2[0]	    
	    pc= sample(range(len(cromo_1)),2)
	    pc.sort()
	    pc1,pc2 = pc
	    f1= cromo_1[:pc1] + cromo_2[pc1:pc2] + cromo_1[pc2:]
	    f2= cromo_2[:pc1] + cromo_1[pc1:pc2] + cromo_2[pc2:]
	    return ((f1,0),(f2,0))
	else:
	    return (indiv_1,indiv_2)
	
def uniform_cross(indiv_1, indiv_2,prob_cross):
    value = random()
    if value < prob_cross:
        cromo_1 = indiv_1[0]
        cromo_2 = indiv_2[0]
        f1=[]
        f2=[]
        for i in range(0,len(cromo_1)):
            if random() < 0.5:
                f1.append(cromo_1[i])
                f2.append(cromo_2[i])
            else:
                f1.append(cromo_2[i])
                f2.append(cromo_1[i])
        return ((f1,0),(f2,0))
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

def one_tour(population,size):
    """Minimization Problem. Deterministic"""
    pool = sample(population, size)
    pool.sort(key=itemgetter(1), reverse=False)
    return pool[0]


# Survivals Selection: elitism
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
def best_pop(population):
    population.sort(key=itemgetter(1),reverse=False)
    return population[0]

def average_pop(population):
    return sum([fit for cromo,fit in population])/len(population)