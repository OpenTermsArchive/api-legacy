import os

CGUS_DATASET_PATH = "./dataset/"
DATASET_DATE_FORMAT = "%Y-%m-%d--%H-%M-%S"
RATE_LIMIT = "10000/minute"

CGUS_API_ENV = os.getenv("CGUS_API_ENV", "development")
BASE_PATH = "/api/open-terms-archive" if CGUS_API_ENV == "production" else ""
