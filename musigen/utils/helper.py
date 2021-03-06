def int_from_bits(bits: list[int]) -> int:
    return int(sum(bit * pow(2, index) for index, bit in enumerate(bits)))


def get_fitness_score() -> int:
    try:
        rating_input = input("Rating (0-5)")
        rating = int(rating_input)
    except ValueError:
        rating = 0

    return rating
