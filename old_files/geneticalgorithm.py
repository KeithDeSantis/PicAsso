import copy
import time
import random
import heapq
from typing import Union
from tqdm import tqdm


def generator(start_time, run_time):
    while time.time() - start_time < run_time:
        yield


''' Default mutation chance function, 1/10000 chance '''
def small_chance(organism):
    return random.randint(0, 9999) == 0

''' 5% chance '''
def five_percent_chance(organism):
    return random.randint(0, 99) < 5

def always(org):
    return True

def good_chance(organism):
    return random.randint(1, 2) == 1

''' Default selection function, weighted choice based on fitness '''
def basic_fitness_selection(population, minimum_fitness):
    fitnesses = map(lambda org: org.fitness + abs(minimum_fitness) + 1, population)
    return random.choices(population, weights=list(fitnesses), k=1)[0]

def power_fitness_selection(population, minimum_fitness, power=2, offset=3):
    fitnesses = map(lambda org: pow(org.fitness, 2) + abs(minimum_fitness) + 1 + offset, population)
    return random.choices(population, weights=list(fitnesses), k=1)[0]

def random_selection(population, minimum_fitness):
    return random.choice(population)


class GeneticAlgorithm:
    def __init__(self,
                 pop_size,
                 initial_population,
                 selection_function=basic_fitness_selection,
                 should_mutate_function=five_percent_chance,
                 elitism_factor: Union[int, float] = 0,
                 culling_factor: Union[int, float] = 0
                 ):
        self.pop_size = pop_size
        self.population = initial_population.copy()
        self.next_population = []
        self.select = selection_function
        self.should_mutate = should_mutate_function
        ''' If these factors are < 1, treat them as a PERCENT
            If they are <= 1, treat them as a NUMBER OF ORGANISMS '''
        self.elitism_factor = elitism_factor
        self.culling_factor = culling_factor

        self.current_generation = -1
        ''' Contains the best organism from each generation. 
            Generation 0 is the initial population '''
        self.best_per_generation = []
        self.worst_per_generation = []
        self.median_per_generation = []
        self.best_org_generation = -1
        self.best_org = self.most_fit()
        pass

    ''' Copy the best from the current population into the next population,
        as determined by the elitism factor '''

    def elitism(self):
        num = self.elitism_factor
        if num < 1:
            num = int(num * self.pop_size)
        elite = self.most_fit(num)
        if num == 1:  # elite is just an organism
            self.next_population.append(elite)
        else:  # elite is a list of organisms
            self.next_population.extend(elite)

    ''' Remove the worst from the current population 
        as determined by the culling factor '''

    def culling(self):
        num = self.culling_factor
        if num < 1:
            num = int(num * self.pop_size)
        heapq.heapify(self.population)
        for i in range(num):
            heapq.heappop(self.population)

    ''' Selects two different parents from the current population 
        based on the selection function given in the constructor '''

    def select_parents(self):
        parent1 = self.select(self.population, self.min_fitness)
        parent2 = self.select(self.population, self.min_fitness)
        count = 0  # limit the iterations on the while loop
        while (parent2 is parent1) and count < self.pop_size:  # should we check if they are the same object (is) or equal (==) ?
            parent2 = self.select(self.population, self.min_fitness)
            count += 1
        return parent1, parent2

    ''' Mutates the organism if it should based on the should_mutate function '''

    def chance_mutate(self, organism):
        if self.should_mutate(organism):
            organism.mutate()

    ''' Returns the n most fit organisms in the current population'''

    def most_fit(self, n=1):
        heapq.heapify(self.population)
        if n == 1:
            return heapq.nlargest(n, self.population)[0]
        return heapq.nlargest(n, self.population)

    ''' Returns the least fit organism in the current population '''

    def least_fit(self):
        heapq.heapify(self.population)
        return self.population[0]

    ''' Returns the organism at the bottom of the 50th percentile of fitness '''

    def median_fit(self):
        top50 = self.most_fit(int(self.pop_size / 2))
        return top50[len(top50) - 1]  # the bottom of the 50th percentile

    ''' Returns a list of the best organism per generation '''

    def best_organisms_per_generation(self):
        return self.best_per_generation

    def worst_organisms_per_generation(self):
        return self.worst_per_generation

    def middle_organisms_per_generation(self):
        return self.median_per_generation

    def run(self, run_time):
        start_time = time.time()
        for _ in tqdm(generator(start_time, run_time)):
            self.current_generation += 1
            # print("Top fitness " + str(self.most_fit().fitness()))
            self.best_per_generation.append(self.most_fit())
            if self.best_per_generation[-1].fitness > self.best_org.fitness: # this will be adjusted when we're ont tracking these lists
                self.best_org_generation = self.current_generation
                self.best_org = self.best_per_generation[-1]
            self.worst_per_generation.append(self.least_fit())
            self.min_fitness = self.worst_per_generation[-1].fitness # this will be adjusted when we're ont tracking these lists
            self.median_per_generation.append(self.median_fit())
            self.elitism()
            self.culling()
            ''' Checking if < self.pop_size could be problematic if adding two children
                at once and pop_size is not even. If too big could just trim the end '''
            while len(self.next_population) < self.pop_size:
                parent1, parent2 = self.select_parents()
                child1, child2 = parent1.crossover(parent2)
                self.chance_mutate(child1)
                self.chance_mutate(child2)
                # TODO do we only add children with better fitness than their parents to the next population?
                # would this make the program essentially unrunnable
                self.next_population.append(child1)
                self.next_population.append(child2)
            self.population = self.next_population
            self.next_population = []

        # we are now done, don't forget to add the new guys from the last round!
        self.best_per_generation.append(self.most_fit())
        self.worst_per_generation.append(self.least_fit())
        self.median_per_generation.append(self.median_fit())
        return self.most_fit()
        pass


if __name__ == "__main__":
    print("Hello World")
