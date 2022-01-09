import os

from midiutil import MIDIFile

from musigen.algo.algo import Genome

from musigen.player.player import MusicPlayer as player
from musigen.player.player import Score


def save_genome_to_midi(filename: str, genome: Genome, tune: Score):
    melody = player.genome_to_melody(genome, tune)

    if len(melody["notes"][0]) != len(melody["beat"]) or len(melody["notes"][0]) != len(
        melody["velocity"]
    ):
        raise ValueError

    mf = MIDIFile()

    track = 0
    channel = 0
    time = 0.0
    
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, tune.bpm)

    for i, vel in enumerate(melody["velocity"]):
        if vel > 0:
            for step in melody["notes"]:
                mf.addNote(track, channel, step[i], time, melody["beat"][i], vel)

        time += melody["beat"][i]

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        mf.writeFile(f)
