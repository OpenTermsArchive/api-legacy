import os

CGUS_DATASET_PATH = "./dataset/"
DATASET_DATE_FORMAT = "%Y-%m-%d--%H-%M-%S"
RATE_LIMIT = "10000/minute"

OTA_API_ENV = os.getenv("OTA_API_ENV", "development")
ENV_MAPPING = {
    "production": "/api/open-terms-archive",
    "preproduction": "/api/open-terms-archive-preprod",
    "development": "",
}
BASE_PATH = ENV_MAPPING.get("OTA_API_ENV", "")
