from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from config import CGUS_DATASET_PATH, RATE_LIMIT, BASE_PATH
from dataset_parser import CGUsFirstOccurenceParser

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(openapi_url=f"{BASE_PATH}/openapi.json",
              docs_url=f"{BASE_PATH}/docs")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get(f"{BASE_PATH}/")
@limiter.limit(RATE_LIMIT)
async def index(request: Request):
    return RedirectResponse(f"{BASE_PATH}/docs")


@app.get(f"{BASE_PATH}/first_occurence/v1/{{term}}")
@limiter.limit(RATE_LIMIT)
async def first_occurence(request: Request, term: str):
    parser = CGUsFirstOccurenceParser(Path(CGUS_DATASET_PATH), term)
    parser.run()
    return parser.to_dict()
