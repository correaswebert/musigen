from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


def decodeUrl(url: str):
    url_data = url.split("-")
    bpm = url_data.pop()
    scale = url_data.pop()
    grid = [int(row, 16) for row in url_data]
    return grid, scale, bpm

def encodeUrl(grid, scale, bpm):
    grid = [hex(row)[2:] for row in grid]
    url = "-".join(map(str, grid))
    url += f"-{scale}-{bpm}"
    return url


@app.get("/{synthpad_data_url}")
def read_item(synthpad_data_url: str):
    grid, scale, bpm = decodeUrl(synthpad_data_url)
    # do some magic...
    return encodeUrl(grid, scale, bpm)

@app.get("/")
def fn():
    return "something..."
