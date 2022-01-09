import random

from .genome import Genome, generate_genome, genome_to_string


class Population:
    weighted_population: list[Genome] = None
    genomes: list[Genome] = None
    fitness: list[int] = None

    def __len__(self) -> int:
        return len(self.genomes)

    def eval_genome_fitness(self, genome) -> int:
        """Given a genome, find its fitness score if it exists in the population

        :returns: fitness score of the genome
        """

        genome_population_index = self.genomes.index(genome)
        return self.fitness[genome_population_index]

    def pair_selection(self) -> tuple[Genome, Genome]:
        """Randomly select a pair from the weighted population

        :returns: a list of two genomes
        """

        return tuple(random.sample(population=self.weighted_population, k=2))

    def get_genome_fitness(self, index: int) -> int:
        """Get the fitness of genome at given index

        :param index: index of the genome whose fitness to be found
        :returns: fitness score
        """

        return self.fitness[index]

    def generate_weighted_distribution(self) -> list[Genome]:
        """Generate a new population weighted on fitness

        Create multiple copies of a specific genome based on its fitness. Hence, if
        the fitness of genome A is 10, create 10 copies of A in the new population.
        Similarly, if the fitness of genome B is 3, create 3 copies of it.

        :param population: list of genomes
        :param fitness_func: to evaluate genome fitness
        :returns: a new population weighted on fitness
        """

        self.weighted_population: list[Genome] = []

        for genome in self.genomes:
            genome_copies = [genome] * (self.eval_genome_fitness(genome) + 1)
            self.weighted_population.extend(genome_copies)

    def sort_population(self, inplace: bool = False) -> list[Genome]:
        """Sort the genome population based on the provided fitness function

        :param inplace: if True then genomes are sorted inplace
        :returns: population in descending order of fitness
        """

        sorted_genomes = sorted(
            self.genomes, key=self.eval_genome_fitness, reverse=True
        )
        if inplace:
            self.genomes = sorted_genomes
        return sorted_genomes

    def generate_population(self, population_size: int, genome_length: int):
        """Generates multiple genomes to form a population

        :param population_size: number of genomes to be generated
        :param genome_length: length of genome sequence
        """

        self.genomes = [generate_genome(genome_length) for _ in range(population_size)]
        self.fitness = [0] * population_size

    def population_fitness(self) -> int:
        """Calculate population fitness by summing individual genome fitness

        :param population: population of genomes
        :param fitness_fn: used to calculate fitness of genome
        :returns: sum of fitness score of all genomes in population
        """

        return sum(self.fitness)

    def print_stats(self, generation_id: int):
        """Print population stats"""
        sorted_population = self.sort_population()

        print(
            f"GENERATION {generation_id:02d}",
            "=============",
            f"Population: [{', '.join([genome_to_string(gene) for gene in self.genomes])}]",
            f"Avg. Fitness: {(self.population_fitness() / len(self))}",
            f"Best: {genome_to_string(sorted_population[0])} ({self.get_genome_fitness(0)})",
            f"Worst: {genome_to_string(sorted_population[-1])} ({self.get_genome_fitness(-1)})",
            sep="\n"
        )