import datetime
import random
from pathlib import Path

import pyo

from musigen.algo.evolution import Evolution
from musigen.algo.population import Population
from musigen.misc.helper import get_fitness_score
from musigen.player.midi import save_genome_to_midi
from musigen.player.player import MusicPlayer, Tune


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

    dirname = Path(f"./midi/{datetime.datetime.now():%d-%m-%Y-%H-%M}")
    s = pyo.Server().boot()

    tune = Tune(num_bars, num_notes, num_steps, pauses, key, scale, root, bpm)

    player = MusicPlayer()

    evo = Evolution(
        mutation_probability=mutation_probability,
        num_mutation_rounds=num_mutations,
        fitness_limit=5,
        generation_limit=3,
    )

    ppl = Population()
    ppl.generate_population(
        population_size=population_size,
        genome_length=(num_bars * num_notes * MusicPlayer.BITS_PER_NOTE),
    )

    population_id = 0
    while True:
        random.shuffle(ppl.genomes)

        # generate fitness scores
        for i, genome in enumerate(ppl.genomes):
            player.play_tune(genome, s, tune)
            ppl.fitness[i] = get_fitness_score()

        evo.run_evolution(ppl, generate_stats=True)
        print(f"population {population_id} done")

        print("Here is the best tune")
        player.play_tune(ppl.genomes[0], s, tune)

        print("saving population midi …")
        for i, genome in enumerate(ppl.genomes):
            filename = f"{scale}-{key}-{i}.mid"
            filepath = dirname / f"{population_id}" / filename
            save_genome_to_midi(filepath, genome, tune)
        print("done")

        if input("continue? [Y/n]").lower() != "y":
            break

        population_id += 1


if __name__ == "__main__":
    main()
