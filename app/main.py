from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from config import CGUS_DATASET_PATH, RATE_LIMIT, BASE_PATH
from data_finder import CGUsDataFinder
from dataset_parser import CGUsFirstOccurenceParser, CGUsAllOccurencesParser, CGUsDataset
from utils import parse_user_date

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(openapi_url=f"{BASE_PATH}/openapi.json",
              docs_url=f"{BASE_PATH}/docs")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(f"{BASE_PATH}/")
@limiter.limit(RATE_LIMIT)
async def index(request: Request):
    return RedirectResponse(f"{BASE_PATH}/docs")


@app.get(f"{BASE_PATH}/first_occurence/v1/{{term}}")
@limiter.limit(RATE_LIMIT)
async def first_occurence(request: Request, term: str):
    """
    Returns the date of first occurence of a given term for every (Service - Document Type) pair.
    Search for multiple terms by separating them with a comma (e.g. "rgpd,trackers,cookies").
    Search is case-insensitive. `false` is returned if the term is not found.
    """
    parser = CGUsFirstOccurenceParser(Path(CGUS_DATASET_PATH), term)
    parser.run()
    return parser.to_dict()

@app.get(f"{BASE_PATH}/all_occurences/v1/{{term}}")
@limiter.limit(RATE_LIMIT)
async def all_occurence(request: Request, term: str):
    """
    Returns whether a version in the dataset contains a given term.
    Search for multiple terms by separating them with a comma (e.g. "rgpd,trackers,cookies").
    Search is case-insensitive.
    """
    parser = CGUsAllOccurencesParser(Path(CGUS_DATASET_PATH), term)
    parser.run()
    return parser.to_dict()

@app.get(f"{BASE_PATH}/list_services/v1/")
@limiter.limit(RATE_LIMIT)
async def list_services(request: Request, multiple_versions_only: bool = False):
    """
    Returns a JSON object with services as keys and a list of their available document types.
    multiple_versions_only: filters out service-document pairs for which only one version is recorded
    """
    dataset = CGUsDataset(Path(CGUS_DATASET_PATH))
    return dataset.list_all_services_doc_types(multiple_versions_only=multiple_versions_only)
    
@app.get(f"{BASE_PATH}/get_version_at_date/v1/{{service}}/{{document_type}}/{{date}}")
@limiter.limit(RATE_LIMIT)
async def get_version_at_date(request: Request, service: str, document_type: str, date: str):
    """
    Returns a the version for a given service and a given document type as it was on a certain date.

    The expected date format is YYYY-MM-DD.

    Example : 
    /get_version_at_date/v1/Facebook/Terms of Service/2020-08-13

    {
        "service": "Facebook",
        "doc_type": "Terms of Service",
        "date": "2010-08-13T00:00:00",
        "version_at_date": "2020-08-12T14:30:11"
        "data": "Terms of Service. Welcome to Facebook! For messaging, voice and video, ..."
        "next_version": "2020-09-03T12:30:05"
    }

    """
    try:
        finder = CGUsDataFinder(service, document_type)
    except Exception as e:
        raise HTTPException(400, str(e))
    try:
        parsed_date = parse_user_date(date)
    except ValueError as e:
        raise HTTPException(400, f"Issue parsing date : {str(e)}. Expected format is YYYY-MM-DD.")
    return finder.get_version_at_date(parsed_date)