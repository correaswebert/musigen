import pyo

from ..core.genome import Genome
from ..utils.helper import int_from_bits
from ..utils.logger import Logger
from .tune import TuneMetadata


class Melody:
    def __init__(self, bits_per_note) -> None:
        self.notes: list[list[int]] = []
        self.velocity: list[int] = []
        self.beat: list[float] = []
        self.bits_per_note = bits_per_note
        self.logger = Logger.get_logger()

    def from_genome(self, genome: Genome, tune: TuneMetadata, scale: pyo.EventScale):
        """Converts the data encoded in the genome to musical melody

        :param genome: the genome encoding the melody
        :param tune: dataclass containing tune metadata
        """

        note_length = 4 / tune.num_notes
        pause_threshhold = 1 << (self.bits_per_note - 1)

        # default unattainable value to remove length check (remove later)
        note_values: list[int] = [-1]

        # break genome into list of its subsequences (encoding musical notes)
        genome_chunks = [
            genome[i * self.bits_per_note : (i + 1) * self.bits_per_note]
            for i in range(tune.num_bars * tune.num_notes)
        ]

        for genome_chunk in genome_chunks:
            subsequence_value = int_from_bits(genome_chunk)

            if not tune.pauses:
                subsequence_value %= pause_threshhold

            # generates a pause
            if subsequence_value >= pause_threshhold:
                note_values.append(0)
                self.velocity.append(0)
                self.beat.append(note_length)

            else:
                # prolong the previous note if same note_value
                if note_values[-1] == subsequence_value:
                    self.beat[-1] += note_length
                else:
                    note_values.append(subsequence_value)
                    self.velocity.append(127)
                    self.beat.append(note_length)

        note_values.remove(-1)

        for step in range(tune.num_steps):
            note = [
                int(scale[(note_value + step * 2) % len(scale)])
                for note_value in note_values
            ]
            self.notes.append(note)
