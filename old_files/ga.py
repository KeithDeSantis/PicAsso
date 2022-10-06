import sys
import imageboard
from imageboard import *
import old_files.geneticalgorithm as geneticalgorithm
from old_files.geneticalgorithm import *

def ga(pool, runtime):

    run_time = float(runtime)

    pop = []

    #------Parameters-------#
    crossover_function = imageboard.crossover_sectional # the function used for crossover
    mutation_function = imageboard.mutation_normal # the function used for mutation
    fitness_function = imageboard.neighbor_based_fitness # the function used to determine fitness
    selection_function = geneticalgorithm.basic_fitness_selection # GA's selection function
    should_mutate_function = geneticalgorithm.good_chance # GA's should_mutate function
    number_crossovers = 2

    pop_size = 100
    ga_elitism_factor = 2
    ga_culling_factor = 0.2
    
    for org in range(pop_size):
        pop.append(ImageBoard(pool,
                crossover_function=crossover_function, # the function used for crossover
                mutation_function=mutation_function, # the function used for mutation
                fitness_function=fitness_function, # the function used to determine fitness
                number_crossovers=number_crossovers # the number of crossovers done per child production
                ))

    ga = GeneticAlgorithm(len(pop),
                            pop,
                            selection_function=selection_function,
                            should_mutate_function=should_mutate_function,
                            elitism_factor=ga_elitism_factor,
                            culling_factor=ga_culling_factor)

    top_organism = ga.run(run_time)

    print("Top Organism: \n" + str(top_organism))
    print("Score: " + str(top_organism.fitness))
    print("Number of generations run: " + str(ga.current_generation + 1))
    print("Best organism found at generation " + str(ga.best_org_generation + 1))

    return top_organism

if __name__ == "__main__":
    pool =[]
    for color in range(pop_size):
        pool.append(int(hex(random.randint(0,16777215)), base=16))
    ga(pool, 10)