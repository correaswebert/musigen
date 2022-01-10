from dataclasses import dataclass


@dataclass
class TuneMetadata:
    num_bars: int
    num_notes: int
    num_steps: int
    pauses: bool
    key: str
    scale: str
    root: int
    bpm: int
