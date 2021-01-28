from datetime import datetime

def parse_user_date(user_date: str):
    '''
    For now, the only allowed format is %Y-%m-%d
    Returns a datetime which is the date at 23:59:59
    '''
    parsed_datetime = (
        datetime.strptime(user_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=59)
    )
    return parsed_datetime