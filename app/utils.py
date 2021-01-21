from datetime import datetime

def parse_user_date(user_date: str):
    '''
    For now, the only allowed format is %Y-%m-%d
    '''
    parsed_datetime = datetime.strptime(user_date, "%Y-%m-%d")
    return parsed_datetime