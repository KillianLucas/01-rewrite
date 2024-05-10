import os
import time
from dateutil import parser
from dateutil.relativedelta import relativedelta
import parsedatetime as pdt
import datetime

def schedule(time_string, code):
    """
    This function takes a time string and a piece of code, and creates a new Python file in the 'schedule' directory.
    The time string should be in the format 'every <day_of_week> at <hour>:<minute>', e.g. 'every friday at 14:00'.
    The created file will include the provided code and will be named according to the convention '<unix_time_to_start>_<interval_in_seconds>'.
    For example, a file named '10_25' would start at Unix time 10 and repeat every 25 seconds.
    """
    # Parse the time string
    cal = pdt.Calendar()
    time_struct, parse_status = cal.parse(time_string)
    dt = datetime.datetime(*time_struct[:6])

    # Calculate the Unix time to start
    unix_time_to_start = int(time.mktime(dt.timetuple()))

    # Calculate the interval in seconds
    interval_in_seconds = relativedelta(dt, datetime.datetime.now()).total_seconds()

    # Create the file in the 'schedule' directory
    filename = f"{unix_time_to_start}_{interval_in_seconds}"
    with open(os.path.join("..", "schedule", filename), 'w') as f:
        f.write(code)




