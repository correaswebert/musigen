import random
import time
from datetime import datetime

import pyo

from musigen.algo.algo import (
    Genome,
    generate_genome,
    mutation,
    selection_pair,
    single_point_crossover,
)
from musigen.misc.helper import get_fitness_score
from musigen.player.midi import save_genome_to_midi
from musigen.player.player import MusicPlayer
from musigen.player.player import Tune


def main():
    num_bars = 8
    num_notes = 4
    num_steps = 1
    pauses = True
    key = "C"
    scale = "major"
    root = 4
    population_size = 1
    num_mutations = 2
    mutation_probability = 0.5
    bpm = 128

    folder_name = str(int(datetime.now().timestamp()))
    s = pyo.Server().boot()

    tune = Tune(num_bars, num_notes, num_steps, pauses, key, scale, root, bpm)

    population_id = 0
    population = [
        generate_genome(num_bars * num_notes * MusicPlayer.BITS_PER_NOTE)
        for _ in range(population_size)
    ]

    player = MusicPlayer()

    while True:
        random.shuffle(population)

        # generate fitness scores
        population_fitness: list[tuple[Genome, int]] = []
        for genome in population:
            player.play_tune(genome, s, tune)
            genome_fitness_score = get_fitness_score()
            population_fitness.append((genome, genome_fitness_score))

        sorted_population_fitness = sorted(
            population_fitness, key=lambda e: e[1], reverse=True
        )

        population = [e[0] for e in sorted_population_fitness]

        next_generation = population[:2]

        for _ in range(len(population) // 2 - 1):

            def fitness_lookup(genome):
                for e in population_fitness:
                    if e[0] == genome:
                        return e[1]
                return 0

            parents = selection_pair(population, fitness_lookup)
            offspring_a, offspring_b = single_point_crossover(parents[0], parents[1])
            offspring_a = mutation(
                offspring_a,
                number_of_mutation_rounds=num_mutations,
                mutation_probability=mutation_probability,
            )
            offspring_b = mutation(
                offspring_b,
                number_of_mutation_rounds=num_mutations,
                mutation_probability=mutation_probability,
            )
            next_generation += [offspring_a, offspring_b]

        print(f"population {population_id} done")

        events = player.genome_to_events(population[0], tune)
        for e in events:
            e.play()
        s.start()
        input("here is the no1 hit …")
        s.stop()
        for e in events:
            e.stop()

        time.sleep(1)

        # events = player.genome_to_events(population[1], tune)
        # for e in events:
        #     e.play()
        # s.start()
        # input("here is the second best …")
        # s.stop()
        # for e in events:
        #     e.stop()

        # time.sleep(1)

        print("saving population midi …")
        for i, genome in enumerate(population):
            filepath = f"{folder_name}/{population_id}/{scale}-{key}-{i}.mid"
            save_genome_to_midi(filepath, genome, tune)
        print("done")

        if input("continue? [Y/n]").lower() == "y":
            break

        population = next_generation
        population_id += 1


if __name__ == "__main__":
    main()
