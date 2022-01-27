import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from musigen.core.evolution import Evolution
from musigen.core.population import Population
from musigen.api.hash import decodeUrl, encodeUrl

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000" "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["get"],
    allow_headers=["*"],
)


def main(grid_hash: str) -> str:
    mutation_probability = 0.5
    num_mutations = 5

    evo = Evolution(
        mutation_probability=mutation_probability,
        num_mutation_rounds=num_mutations,
        fitness_limit=5,
        generation_limit=3,
    )

    ppl = Population.from_hash(grid_hash)
    
    ppl.genomes = evo.run_evolution(ppl)

    return ppl.to_hash()


@app.get("/{synthpad_data_url}")
def read_item(synthpad_data_url: str):
    if synthpad_data_url == "favicon.ico":
        return
    
    grid_hash, scale, bpm = decodeUrl(synthpad_data_url)
    updated_grid_hash = main(grid_hash)

    return encodeUrl(updated_grid_hash, scale, bpm)
