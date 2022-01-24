import datetime
import random
from pathlib import Path
import itertools

from musigen.core.evolution import Evolution
from musigen.core.population import Population
from musigen.misc import helper
from musigen.player import midi
from musigen.player.server import AudioServer
from musigen.player.tune import TuneMetadata
from musigen.misc.logger import Logger


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
    log_filename = "file.log"

    musigen_logger = Logger()
    musigen_logger.add_file_handler(log_filename)
    musigen_logger.add_stream_handler(log_level="DEBUG")

    dirname = Path(f"./midi/{datetime.datetime.now():%d-%m-%Y-%H-%M}")

    tune = TuneMetadata(num_bars, num_notes, num_steps, pauses, key, scale, root, bpm)

    player = AudioServer()

    evo = Evolution(
        mutation_probability=mutation_probability,
        num_mutation_rounds=num_mutations,
        fitness_limit=5,
        generation_limit=3,
    )

    ppl = Population()
    ppl.generate_population(
        population_size=population_size,
        genome_length=(num_bars * num_notes * AudioServer.BITS_PER_NOTE),
    )

    for population_id in itertools.count(start=0):
        try:
            random.shuffle(ppl.genomes)

            # generate fitness scores
            for i, genome in enumerate(ppl.genomes):
                player.play_tune(genome, tune, with_metronome=True)
                ppl.fitness[i] = helper.get_fitness_score()

            evo.run_evolution(ppl)
            ppl.print_stats(population_id)

        except KeyboardInterrupt:
            player.stop_server()
            print()
            break

    print("Playing the best tune generated...")
    player.play_tune(ppl.genomes[0], tune)

    print("Saving the top two tunes...")
    for i, genome in enumerate(ppl.genomes[:2]):
        filename = f"{scale}-{key}-{i}.mid"
        filepath = dirname / f"{population_id}" / filename
        midi.save_genome_data(genome, tune, filepath)

    print("Done.")


if __name__ == "__main__":
    main()
