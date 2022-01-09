from dataclasses import dataclass
import time
from musigen.algo.algo import Genome
from musigen.misc.helper import int_from_bits
import pyo


@dataclass
class Tune:
    num_bars: int
    num_notes: int
    num_steps: int
    pauses: bool
    key: str
    scale: str
    root: int
    bpm: int

@dataclass
class Melody:
    notes: list[int]
    velocity: list[int]
    beat: list[int]


class MusicPlayer:

    BITS_PER_NOTE = 4

    KEYS = [
        "C",
        "C#",
        "Db",
        "D",
        "D#",
        "Eb",
        "E",
        "F",
        "F#",
        "Gb",
        "G",
        "G#",
        "Ab",
        "A",
        "A#",
        "Bb",
        "B",
    ]

    SCALES = [
        "major",
        "minorM",
        "dorian",
        "phrygian",
        "lydian",
        "mixolydian",
        "majorBlues",
        "minorBlues",
    ]

    def genome_to_melody(self, genome: Genome, tune: Tune) -> Melody:
        notes = [
            genome[i * self.BITS_PER_NOTE : i * self.BITS_PER_NOTE + self.BITS_PER_NOTE]
            for i in range(tune.num_bars * tune.num_notes)
        ]

        note_length = 4 / tune.num_notes

        scl = pyo.EventScale(root=tune.key, scale=tune.scale, first=tune.root)

        melody = Melody(notes=[], velocity=[], beat=[])

        for note in notes:
            integer = int_from_bits(note)

            if not tune.pauses:
                integer %= pow(2, self.BITS_PER_NOTE - 1)

            if integer >= pow(2, self.BITS_PER_NOTE - 1):
                melody.notes += [0]
                melody.velocity += [0]
                melody.beat += [note_length]
            else:
                if len(melody.notes) > 0 and melody.notes[-1] == integer:
                    melody.beat[-1] += note_length
                else:
                    melody.notes += [integer]
                    melody.velocity += [127]
                    melody.beat += [note_length]

        steps = []
        for step in range(tune.num_steps):
            steps.append(
                [scl[(note + step * 2) % len(scl)] for note in melody.notes]
            )

        melody.notes = steps
        return melody

    def genome_to_events(self, genome: Genome, tune: Tune) -> list[pyo.Events]:
        melody = self.genome_to_melody(genome, tune)

        return [
            pyo.Events(
                midinote=pyo.EventSeq(step, occurrences=1),
                midivel=pyo.EventSeq(melody.velocity, occurrences=1),
                beat=pyo.EventSeq(melody.beat, occurrences=1),
                attack=0.001,
                decay=0.05,
                sustain=0.5,
                release=0.005,
                bpm=tune.bpm,
            )
            for step in melody.notes
        ]

    def play_tune(self, genome: Genome, s: pyo.Server, tune: Tune, with_metronome: bool = False):
        if with_metronome:
            self.play_metronome(tune.bpm)

        events = self.genome_to_events(genome, tune)
        for e in events:
            e.play()
        s.start()

        rating = input("Rating (0-5)")

        for e in events:
            e.stop()
        s.stop()
        time.sleep(1)

    def play_metronome(self, bpm: int):
        met = pyo.Metro(time=60 / bpm).play()
        t = pyo.CosTable([(0, 0), (50, 1), (200, 0.3), (500, 0)])
        amp = pyo.TrigEnv(met, table=t, dur=0.25, mul=1)
        freq = pyo.Iter(met, choice=[660, 440, 440, 440])
        return pyo.Sine(freq=freq, mul=amp).mix(2).out()
