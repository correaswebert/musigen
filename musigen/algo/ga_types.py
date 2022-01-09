from typing import Callable

Genome = list[int]
Population = list[Genome]
PopulateFunc = Callable[[], Population]
FitnessFunc = Callable[[Genome], int]
SelectionFunc = Callable[[Population, FitnessFunc], tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
PrinterFunc = Callable[[Population, int, FitnessFunc], None]
