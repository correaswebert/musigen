import random
from typing import Optional, Callable

Genome = list[int]
Population = list[Genome]
PopulateFunc = Callable[[], Population]
FitnessFunc = Callable[[Genome], int]
SelectionFunc = Callable[[Population, FitnessFunc], tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
PrinterFunc = Callable[[Population, int, FitnessFunc], None]


class GeneticAlgorithm:

    pass


def generate_genome(length: int) -> Genome:
    """Generates a random sequence of 0s and 1s of given length

    :param length: length of sequence to be generated
    :returns: list of 0s and 1s
    """
    return random.choices([0, 1], k=length)


def generate_population(population_size: int, genome_length: int) -> Population:
    """Generate multiple genomes.

    :param population_size: number of genomes to be generated
    :param genome_length: length of genome sequence
    :returns: a list of genomes
    """
    return [generate_genome(genome_length) for _ in range(population_size)]


def single_point_crossover(genome_a: Genome, genome_b: Genome) -> tuple[Genome, Genome]:
    """Generate genome crossovers to create new genomes.

    A single point is selected in the genome sequence. Both the genomes are cut
    at that point and joint to form a crossover.

    original sequence
    A = a1 a2 a3 a4 a5
    B = b1 b2 b3 b4 b5

    crossover sequence
    A' = a1 a2 b3 b4 b5
    B' = b1 b2 a3 a4 a5

    :param genome_a: first genome
    :param genome_b: second genome
    :returns: a 2-tuple of crossed-over genomes
    """

    if len(genome_a) != len(genome_b):
        raise ValueError("Genomes a and b must be of same length")

    genome_length = len(genome_a)
    if genome_length < 2:
        return genome_a, genome_b

    # cross-over point
    p = random.randint(1, genome_length - 1)
    return genome_a[0:p] + genome_b[p:], genome_b[0:p] + genome_a[p:]


# FIX: parameter genome changes as a side-effect
def mutation(
    genome: Genome,
    number_of_mutation_rounds: int = 1,
    mutation_probability: float = 0.5,
) -> Genome:
    """Mutate the given genome by randomly flipping its bit sequence

    :param genome: genome to be mutated
    :param number_of_mutation_rounds: number of times to flip bits
    :param mutation_probability: probability of bit flip occuring
    :returns: mutated genome
    """

    if number_of_mutation_rounds < 0:
        raise ValueError("Number of mutations can only be positive!")

    for _ in range(number_of_mutation_rounds):
        mutation_bit_index = random.randrange(len(genome))
        if random.random() < mutation_probability:
            genome[mutation_bit_index] ^= 1  # bit flip by XOR with 1

    return genome


def population_fitness(population: Population, fitness_fn: FitnessFunc) -> int:
    """Calculate population fitness by summing individual genome fitness

    :param population: population of genomes
    :param fitness_fn: used to calculate fitness of genome
    :returns: population fitness
    """
    return sum(fitness_fn(genome) for genome in population)


def generate_weighted_distribution(
    population: Population, fitness_func: FitnessFunc
) -> Population:
    result: Population = []

    for gene in population:
        gene_variation = [gene] * (fitness_func(gene) + 1)
        result.extend(gene_variation)

    return result


def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return random.sample(
        population=generate_weighted_distribution(population, fitness_func), k=2
    )


def sort_population(population: Population, fitness_func: FitnessFunc) -> Population:
    return sorted(population, key=fitness_func, reverse=True)


def genome_to_string(genome: Genome) -> str:
    return "".join(map(str, genome))


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


def run_evolution(
    populate_fn: PopulateFunc,
    fitness_fn: FitnessFunc,
    fitness_limit: int,
    selection_fn: SelectionFunc = selection_pair,
    crossover_fn: CrossoverFunc = single_point_crossover,
    mutation_fn: MutationFunc = mutation,
    generation_limit: int = 100,
    printer: Optional[PrinterFunc] = None,
) -> tuple[Population, int]:
    """Runs the evolution process
    
    """
    
    population: Population = populate_fn()

    for iteration in range(generation_limit):
        population = sorted(
            population, key=lambda genome: fitness_fn(genome), reverse=True
        )

        if printer is not None:
            printer(population, iteration, fitness_fn)

        if fitness_fn(population[0]) >= fitness_limit:
            return population, iteration

        next_generation = population[0:2]

        for _ in range(len(population) // 2 - 1):
            parents = selection_fn(population, fitness_fn)
            offspring_a, offspring_b = crossover_fn(parents[0], parents[1])
            offspring_a = mutation_fn(offspring_a)
            offspring_b = mutation_fn(offspring_b)
            next_generation.extend([offspring_a, offspring_b])

        population = next_generation

    return population, generation_limit
