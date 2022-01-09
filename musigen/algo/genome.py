import random

Genome = list[int]


def generate_genome(length: int) -> Genome:
    """Generates a random sequence of 0s and 1s of given length

    :param length: length of sequence to be generated
    :returns: list of 0s and 1s
    """
    return random.choices([0, 1], k=length)


def genome_to_string(genome: Genome) -> str:
    return "".join(map(str, genome))
