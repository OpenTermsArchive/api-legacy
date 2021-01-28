from datetime import datetime
import sys
sys.path.append("./app/")

import pytest

from app.utils import parse_user_date

def test_parse_date():
    date = parse_user_date("2020-10-31")
    assert date == datetime(2020, 10, 31, 23, 59, 59, 59)

def test_parse_date_wrong_format():
    with pytest.raises(ValueError):
        date = parse_user_date("2020/10/31")
    with pytest.raises(ValueError):
        date = parse_user_date("2020_10_31")
    with pytest.raises(ValueError):
        date = parse_user_date("2020-11-31")

def test_parse_date_comparison():
    date = parse_user_date("2020-10-31")
    assert date >= datetime(2020, 10, 31, 9, 59, 59, 59)
    assert date >= datetime(2020, 10, 31, 23, 59, 59, 59)