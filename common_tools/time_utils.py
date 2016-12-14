from time import timezone
from datetime import datetime, timedelta


def datetime_string_to_timezone_aware_string(datetime_string):
    """
    Given a datetime as a string, convert into a datetime with the timezone taken into account

    :param datetime_string: String (in format YEAR-MONTH-DAY HOUR:MINUTE:SECOND
    :return: String
    """

    # Get the timestamp as a datetime object instead of a string
    timestamp = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')

    # Get the timezone difference in hours
    timezone_hours = timezone / 60 / 60

    # Get the difference between the timestamp and the timezone
    current_time = timestamp - timedelta(hours=timezone_hours)

    # Return the result, formatted as a string
    return current_time.strftime("%b %d, %Y - %I:%M %p")


def datetime_string_to_timezone_aware_string_tactic_formatted(datetime_string):
    """
    Works the same as datetime_string_to_timezone_aware_string, but returns the string in the same format that TACTIC
    uses for its database.

    :param datetime_string: String (in format YEAR-MONTH-DAY HOUR:MINUTE:SECOND
    :return: String
    """

    # Get the timestamp as a datetime object instead of a string
    timestamp = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')

    # Get the timezone difference in hours
    timezone_hours = timezone / 60 / 60

    # Get the difference between the timestamp and the timezone
    current_time = timestamp - timedelta(hours=timezone_hours)

    # Return the result, formatted as a string
    return current_time.strftime('%Y-%m-%d %H:%M:%S')
