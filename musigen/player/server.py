import pyo

from ..algo.genome import Genome
from .melody import Melody
from .tune import TuneMetadata


class AudioServer:

    BITS_PER_NOTE = 4
    ATTACK = 0.001
    DECAY = 0.05
    SUSTAIN = 0.5
    RELEASE = 0.005

    def __init__(self) -> None:
        self.server = pyo.Server().boot()

    def stop_server(self):
        """Stop playback on the pyo server"""

        self.server.stop()

    def genome_to_events(
        self, genome: Genome, tune_md: TuneMetadata
    ) -> list[pyo.Events]:
        """Generates pyo events corresponding to the melody encoded by the genome

        :param genome: the genome encoding the melody
        :param tune: dataclass containing tune metadata
        :returns: pyo events encoding the melody
        """

        scale = pyo.EventScale(
            root=tune_md.key, scale=tune_md.scale, first=tune_md.root
        )
        melody = Melody(bits_per_note=self.BITS_PER_NOTE)
        melody.from_genome(genome, tune_md, scale)

        return [
            pyo.Events(
                midinote=pyo.EventSeq(note, occurrences=1),
                midivel=pyo.EventSeq(melody.velocity, occurrences=1),
                beat=pyo.EventSeq(melody.beat, occurrences=1),
                attack=self.ATTACK,
                decay=self.DECAY,
                sustain=self.SUSTAIN,
                release=self.RELEASE,
                bpm=tune_md.bpm,
            )
            for note in melody.notes
        ]

    def play_tune(
        self,
        genome: Genome,
        tune_md: TuneMetadata,
        with_metronome: bool = False,
    ):
        """Plays the melody encoded by the genome

        :param genome: the genome encoding the melody
        :param s: pyo server used for interfacing with audio card
        :param with_metronome: if true then metronome also played
        """

        if with_metronome:
            self.play_metronome(tune_md.bpm)

        events = self.genome_to_events(genome, tune_md)
        for e in events:
            e.play()
        self.server.start()

        input("Press ENTER to stop playback")

        for e in events:
            e.stop()
        self.server.stop()

    @staticmethod
    def play_metronome(bpm: int) -> pyo.Sine:
        """Plays the metronome for the given beat count

        :param bpm: beat count
        """

        met = pyo.Metro(time=60 / bpm).play()
        t = pyo.CosTable([(0, 0), (50, 1), (200, 0.3), (500, 0)])
        amp = pyo.TrigEnv(met, table=t, dur=0.25, mul=1)
        freq = pyo.Iter(met, choice=[660, 440, 440, 440])

        pyo.Sine(freq=freq, mul=amp).mix(2).out()
