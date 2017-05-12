"""
sea_bin_visual.py
A very simple EA for binary representation.
Ernesto Costa
Adjusted by Sebastian Rehfeldt
"""


from random import random,randint, sample, seed, choice
from operator import itemgetter

def run(numb_runs,numb_generations,size_pop, size_cromo, prob_mut, prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
    statistics = []
    for i in range(numb_runs):
        seed(i)
        best, stat_best, stat_aver = sea_for_plot(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func)
        statistics.append(stat_best)
    stat_gener = list(zip(*statistics))
    boa = [min(g_i) for g_i in stat_gener] # minimization
    aver_gener =  [sum(g_i)/len(g_i) for g_i in stat_gener]
    return boa, aver_gener

# Simple [Binary] Evolutionary Algorithm		
def sea(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
    # inicialize population: indiv = (cromo,fit)
    populacao = gera_pop(size_pop,size_cromo)
    # evaluate population
    populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao]
    for i in range(numb_generations):
        # sparents selection
        mate_pool = sel_parents(populacao)
	# Variation
	# ------ Crossover
        progenitores = []
        for i in  range(0,size_pop-1,2):
            indiv_1= mate_pool[i]
            indiv_2 = mate_pool[i+1]
            filhos = recombination(indiv_1,indiv_2, prob_cross)
            progenitores.extend(filhos) 
        # ------ Mutation
        descendentes = []
        for indiv,fit in progenitores:
            novo_indiv = mutation(indiv,prob_mut)
            descendentes.append((novo_indiv,fitness_func(novo_indiv)))
        # New population
        populacao = sel_survivors(populacao,descendentes)
        # Evaluate the new population
        populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao]     
    return best_pop(populacao)


# Simple [Binary] Evolutionary Algorithm 
# Return the best plus, best by generation, average population by generation
def sea_for_plot(numb_generations,size_pop, size_cromo, prob_mut,prob_cross,sel_parents,recombination,mutation,sel_survivors, fitness_func):
    # inicializa populacao: indiv = (cromo,fit)
    populacao = gera_pop(size_pop,size_cromo)
    #print([sum(indiv[0]) for indiv in populacao])
    # avalia populacao
    populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao]

    # para a estatistica
    stat = [best_pop(populacao)[1]]
    stat_aver = [average_pop(populacao)]
    
    for i in range(numb_generations):
        # selecciona progenitores
        mate_pool = sel_parents(populacao)
    # Variation
    # ------ Crossover
        progenitores = []
        for i in  range(0,size_pop-1,2):
            cromo_1= mate_pool[i]
            cromo_2 = mate_pool[i+1]
            filhos = recombination(cromo_1,cromo_2, prob_cross)
            filhos = fix_sizes(filhos)
            progenitores.extend(filhos) 
        # ------ Mutation
        descendentes = []
        for indiv,fit in progenitores:
            novo_indiv = mutation(indiv,prob_mut)
            descendentes.append((novo_indiv,fitness_func(novo_indiv)))
        # New population
        populacao = sel_survivors(populacao,descendentes)
        # Avalia nova _populacao
        populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao] 
    
    # Estatistica
        stat.append(best_pop(populacao)[1])
        stat_aver.append(average_pop(populacao))
    
    return best_pop(populacao),stat, stat_aver


# Initialize population
def gera_pop(size_pop,size_cromo):
    return [(gera_indiv(size_cromo),0) for i in range(size_pop)]

def gera_indiv(size_cromo):
    #creates initial population with equal sized sets
    indiv = [randint(0,1) for i in range(size_cromo)]
    indiv = fix_sizes([(indiv,0)])
    indiv = indiv[0][0]

    if not sum(indiv)==size_cromo/2:
        print(indiv)
        print(1/0)

    return indiv

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
	    
def fix_sizes(pop):
    fixed = []
    for indiv in pop:
        while sum(indiv[0])>len(indiv[0])/2:
            #flip ones to zeros
            indices = [i for i in range(len(indiv[0])) if indiv[0][i] == 1]
            indiv[0][choice(indices)] = 0

        while sum(indiv[0])<len(indiv[0])/2:
            #flip zeros to ones
            indices = [i for i in range(len(indiv[0])) if indiv[0][i] == 0]
            indiv[0][choice(indices)] = 1

        fixed.append(indiv)

        if not sum(indiv[0])==len(indiv[0])/2:
            print(indiv)
            print(1/0)

    return fixed



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
def best_pop(populacao):
    populacao.sort(key=itemgetter(1),reverse=False)
    return populacao[0]

def average_pop(populacao):
    return sum([fit for cromo,fit in populacao])/len(populacao)