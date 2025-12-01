import datetime

def get_time_index(input_date: datetime):

    indexes = {
        'year': None,
        'week_index': None,
        'year_week': None
    }

    if input_date:
        indexes['year'] = input_date.year
        indexes['week_index'] = int(input_date.strftime("%V"))
        indexes['year_week'] = (indexes['year'] * 100) + indexes['week_index']

    return indexes