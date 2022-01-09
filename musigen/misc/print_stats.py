from typing import Callable
from musigen.algo.algo import Population, FitnessFunc, genome_to_string, population_fitness, sort_population

PrinterFunc = Callable[[Population, int, FitnessFunc], None]


def print_stats(population: Population, generation_id: int, fitness_func: FitnessFunc):
    print(f"GENERATION {generation_id:02d}")
    print("=============")
    print(f"Population: [{', '.join([genome_to_string(gene) for gene in population])}]")
    print(
        f"Avg. Fitness: {(population_fitness(population, fitness_func) / len(population))}"
    )
    sorted_population = sort_population(population, fitness_func)
    print(
        f"Best: {genome_to_string(sorted_population[0])} ({fitness_func(sorted_population[0])})"
    )
    print(
        "Worst: {genome_to_string(sorted_population[-1])} {%ffitness_func(sorted_population[-1]}))"
    )
    print()

    return sorted_population[0]
