import os

CGUS_DATASET_PATH = "./dataset/"
DATASET_DATE_FORMAT = "%Y-%m-%d--%H-%M-%S"
RATE_LIMIT = "10000/minute"

CGUS_API_ENV = os.getenv("CGUS_API_ENV", "development")
ENV_MAPPING = {
    "production": "/api/open-terms-archive",
    "preproduction": "/api/open-terms-archive-preprod",
    "development": "",
}
BASE_PATH = ENV_MAPPING.get("CGUS_API_ENV", "")
