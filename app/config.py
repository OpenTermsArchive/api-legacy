import os

CGUS_DATASET_PATH = "./dataset/"
LAST_DATASET_PATH = "./latest_dataset.txt"
DATASET_DATE_FORMAT = "%Y-%m-%dT%H-%M-%SZ"
RATE_LIMIT = "10000/minute"

BASE_PATH = os.getenv("BASE_PATH", "")

# pylint: disable=line-too-long
DOCTYPE_URL = "https://raw.githubusercontent.com/OpenTermsArchive/terms-types/main/termsTypes.json"
