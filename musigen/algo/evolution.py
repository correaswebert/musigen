import random

from .genome import Genome, genome_to_string
from .population import Population


class Evolution:
    def __init__(
        self,
        mutation_probability: float,
        num_mutation_rounds: int,
        fitness_limit: int,
        generation_limit: int,
    ) -> None:
        self.fitness_limit = fitness_limit
        self.generation_limit = generation_limit
        self.mutation_probability = mutation_probability

        if num_mutation_rounds < 0:
            raise ValueError("Number of mutations can only be positive!")
        self.num_mutation_rounds = num_mutation_rounds

    @staticmethod
    def single_point_crossover(
        genome_pair: tuple[Genome, Genome]
    ) -> tuple[Genome, Genome]:
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

        genome_a, genome_b = genome_pair

        if len(genome_a) != len(genome_b):
            raise ValueError("Genomes a and b must be of same length")

        genome_length = len(genome_a)
        if genome_length < 2:
            return genome_a, genome_b

        # cross-over point
        cpt = random.randint(1, genome_length - 1)
        crossover_genome_a = genome_a[0:cpt] + genome_b[cpt:]
        crossover_genome_b = genome_b[0:cpt] + genome_a[cpt:]

        return [crossover_genome_a, crossover_genome_b]

    # FIX: parameter genome changes as a side-effect
    def create_mutations(self, genome: Genome) -> Genome:
        """Mutate the given genome by randomly flipping its bit sequence

        :param genome: genome to be mutated
        :param number_of_mutation_rounds: number of times to flip bits
        :param mutation_probability: probability of bit flip occuring
        :returns: mutated genome
        """

        for _ in range(self.num_mutation_rounds):
            mutation_bit_index = random.randrange(len(genome))
            if random.random() < self.mutation_probability:
                genome[mutation_bit_index] ^= 1  # bit flip by XOR with 1

        return genome

    def run_evolution(self, ppl: Population) -> list[Genome]:
        """Runs the evolution process creating a new population

        :param ppl: population of genomes
        :param generate_stats: if True then intermediate round stats shown
        """

        # var iteration is function scoped
        ppl.sort_population(inplace=True)

        if ppl.get_genome_fitness(index=0) >= self.fitness_limit:
            return

        # top two genomes of the population carried forward
        next_generation = ppl.genomes[0:2]

        for _ in range(len(ppl) // 2 - 1):
            parents = ppl.pair_selection()
            offspring_a, offspring_b = self.single_point_crossover(parents)

            mutated_offspring_a = self.create_mutations(offspring_a)
            mutated_offspring_b = self.create_mutations(offspring_b)

            next_generation.extend([mutated_offspring_a, mutated_offspring_b])

        return next_generation
