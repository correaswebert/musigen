import os
from pathlib import Path
from posixpath import basename

import pyo
from midiutil import MIDIFile

from ..algo.genome import Genome
from .melody import Melody
from .server import AudioServer
from .tune import TuneMetadata


def save_genome_data(
    genome: Genome,
    tune_md: TuneMetadata,
    filepath: Path,
    track_name: str = "Sample Track",
):
    """Saves the melody of the given genome data in MIDI format

    :param filepath: MIDI file where data will be saved
    :param genome: the genome containing the melody data encoded
    :param tune_md: the tune's metadata
    """

    scale = pyo.EventScale(root=tune_md.key, scale=tune_md.scale, first=tune_md.root)
    melody = Melody(bits_per_note=AudioServer.BITS_PER_NOTE)
    melody.from_genome(genome, tune_md, scale)

    if any(
        (
            len(melody.notes[0]) != len(melody.beat),
            len(melody.notes[0]) != len(melody.velocity),
        )
    ):
        raise ValueError

    track = 0
    channel = 0
    time = 0.0

    midi_file = MIDIFile()
    midi_file.addTrackName(track, time, track_name)
    midi_file.addTempo(track, time, tune_md.bpm)

    for i, vel in enumerate(melody.velocity):
        if vel > 0:
            for step in melody.notes:
                midi_file.addNote(track, channel, step[i], time, melody.beat[i], vel)

        time += melody.beat[i]

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        midi_file.writeFile(f)
