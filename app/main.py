from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from config import CGUS_DATASET_PATH
from dataset_parser import CGUsFirstOccurenceParser

app = FastAPI()

@app.get("/")
async def index():
    return RedirectResponse("/docs")

@app.get("/first_occurence/v1/{term}")
async def first_occurence(term: str):
    parser = CGUsFirstOccurenceParser(Path(CGUS_DATASET_PATH), term)
    parser.run()
    return parser.to_dict()
