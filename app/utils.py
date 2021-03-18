from datetime import datetime
import re


def parse_user_date(user_date: str):
    """
    For now, the only allowed format is %Y-%m-%d
    Returns a datetime which is the date at 23:59:59
    """
    parsed_datetime = datetime.strptime(user_date, "%Y-%m-%d").replace(
        hour=23, minute=59, second=59, microsecond=59
    )
    return parsed_datetime


def parse_date_from_dataset_url(url: str):
    """
    Given a dataset release url,
    Parse and return its date
    """
    date_regex = re.compile("([12]\\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\\d|3[01]))")
    dataset = url.split("/")[-1]
    date = date_regex.search(dataset)
    if date:
        return date.group()
    return "could not parse"
