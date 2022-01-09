import os
from pathlib import Path

from midiutil import MIDIFile

from musigen.algo.algo import Genome

from musigen.player.player import MusicPlayer as player
from musigen.player.player import Tune, Melody


def save_genome_to_midi(filename: Path, genome: Genome, tune: Tune):
    melody: Melody = player().genome_to_melody(genome, tune)

    if len(melody.notes[0]) != len(melody.beat) or len(melody.notes[0]) != len(
        melody.velocity
    ):
        raise ValueError

    midi_file = MIDIFile()

    track = 0
    channel = 0
    time = 0.0
    
    midi_file.addTrackName(track, time, "Sample Track")
    midi_file.addTempo(track, time, tune.bpm)

    for i, vel in enumerate(melody.velocity):
        if vel > 0:
            for step in melody.notes:
                midi_file.addNote(track, channel, step[i], time, melody.beat[i], vel)

        time += melody.beat[i]

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        midi_file.writeFile(f)
