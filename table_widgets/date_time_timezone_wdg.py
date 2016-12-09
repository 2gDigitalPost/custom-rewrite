from pyasm.widget import DateYearTimeWdg

from common_tools.time_utils import datetime_string_to_timezone_aware_string


class DateTimeTimezoneWdg(DateYearTimeWdg):
    def get_display(my):
        timestamp = my.get_value()

        return datetime_string_to_timezone_aware_string(timestamp)
