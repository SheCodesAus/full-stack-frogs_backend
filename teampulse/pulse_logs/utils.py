import datetime
from django.utils import timezone
from django.apps import apps

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

def check_user_has_logged(user, timestamp=None):
    """
    Checks if a user has created a PulseLog for the week of the given timestamp.
    If no timestamp is provided, uses the current time.
    """
    if timestamp is None:
        timestamp = timezone.now()

    indices = get_time_index(timestamp)
    target_year_week = indices.get('year_week')

    if target_year_week:
        PulseLog = apps.get_model('pulse_logs', 'PulseLog')
        return PulseLog.objects.filter(user=user, year_week=target_year_week).exists()

    return False