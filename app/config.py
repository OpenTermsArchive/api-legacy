import os

CGUS_DATASET_PATH = "./dataset/"
LAST_DATASET_PATH = "./latest_dataset.txt"
DATASET_DATE_FORMAT = "%Y-%m-%d--%H-%M-%S"
RATE_LIMIT = "10000/minute"

BASE_PATH = os.getenv("BASE_PATH", "")

DOCTYPE_URL = "https://raw.githubusercontent.com/OpenTermsArchive/services-all/main/document-types.json"
