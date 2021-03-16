# pylint: disable=missing-function-docstring,wrong-import-position
from datetime import datetime
import sys

sys.path.append("./app/")

import pytest

from app.utils import parse_user_date, parse_date_from_dataset_url


def test_parse_date():
    date = parse_user_date("2020-10-31")
    assert date == datetime(2020, 10, 31, 23, 59, 59, 59)


def test_parse_date_wrong_format():
    with pytest.raises(ValueError):
        parse_user_date("2020/10/31")
    with pytest.raises(ValueError):
        parse_user_date("2020_10_31")
    with pytest.raises(ValueError):
        parse_user_date("2020-11-31")


def test_parse_date_comparison():
    date = parse_user_date("2020-10-31")
    assert date >= datetime(2020, 10, 31, 9, 59, 59, 59)
    assert date >= datetime(2020, 10, 31, 23, 59, 59, 59)
    assert date < datetime(2020, 11, 1, 0, 0, 0, 0)


def test_parse_date_from_url():
    url = "https://github.com/releases/download/2021-03-04-fff81e8/dataset-2021-03-04-fff81e8.zip"
    parsed = parse_date_from_dataset_url(url)
    assert parsed == "2021-03-04"


def test_parse_date_from_url_no_date():
    url = "https://google.com"
    parsed = parse_date_from_dataset_url(url)
    assert parsed == "could not parse"


def test_parse_date_from_url_wrong_date_format():
    url = "https://github.com/releases/download/2021-03-04-fff81e8/dataset-04-03-2021-fff81e8.zip"
    parsed = parse_date_from_dataset_url(url)
    assert parsed == "could not parse"
