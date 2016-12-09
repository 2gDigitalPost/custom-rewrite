import time
from datetime import datetime, timedelta

from pyasm.widget import DateYearTimeWdg


class DateTimeTimezoneWdg(DateYearTimeWdg):
    def get_display(my):
        # Get the timestamp as a datetime object instead of a string
        timestamp = datetime.strptime(my.get_value(), '%Y-%m-%d %H:%M:%S')

        # Get the timezone difference in hours
        timezone_hours = time.timezone / 60 / 60

        # Get the difference between the timestamp and the timezone
        current_time = timestamp - timedelta(hours=timezone_hours)

        # Return the result, formatted as a string
        return current_time.strftime("%b %d, %Y - %I:%M %p")
