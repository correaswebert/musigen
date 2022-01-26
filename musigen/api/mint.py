import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from musigen.misc import helper

from ..core.evolution import Evolution
from ..core.population import Population
from .hash import decodeUrl, encodeUrl

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000"
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["get"],
    allow_headers=["*"],
)


def main(grid: list[int]):
    mutation_probability = 0.5
    num_mutations = 5

    evo = Evolution(
        mutation_probability=mutation_probability,
        num_mutation_rounds=num_mutations,
        fitness_limit=5,
        generation_limit=3,
    )

    ppl = Population()
    random.shuffle(ppl.genomes)
    evo.run_evolution(ppl)

    return ppl.genomes


@app.get("/{synthpad_data_url}")
def read_item(synthpad_data_url: str):
    grid, scale, bpm = decodeUrl(synthpad_data_url)

    updated_grid = main(grid)

    return encodeUrl(updated_grid, scale, bpm)
