import datetime
import random
from pathlib import Path
import itertools

from musigen.core.evolution import Evolution
from musigen.core.population import Population
from musigen.utils import helper
from musigen.player import midi
from musigen.player.server import AudioServer
from musigen.player.tune import TuneMetadata
from musigen.utils.logger import Logger


def main():
    musigen_logger = Logger()
    musigen_logger.add_file_handler(filename="file.log")
    musigen_logger.add_stream_handler(log_level="DEBUG")

    outdir_name = Path(f"./midi/{datetime.datetime.now():%d-%m-%Y-%H-%M}")

    tune = TuneMetadata(
        num_bars=8,
        num_notes=4,
        num_steps=1,
        pauses=True,
        key="C",
        scale="major",
        root="4",
        bpm=128,
    )

    evo = Evolution(
        mutation_probability=0.1,
        num_mutation_rounds=2,
        fitness_limit=5,
        generation_limit=3,
    )

    ppl = Population()
    ppl.generate_population(
        population_size=5,
        genome_length=(tune.num_bars * tune.num_notes * AudioServer.BITS_PER_NOTE),
    )

    player = AudioServer()

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
        filename = f"{tune.scale}-{tune.key}-{i}.mid"
        filepath = outdir_name / f"{population_id}" / filename
        midi.save_genome_data(genome, tune, filepath)

    print("Done.")


if __name__ == "__main__":
    main()
