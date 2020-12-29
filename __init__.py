"""
See: https://docs.python.org/3/library/time.html#time.strftime
"""

from collections import namedtuple

###############################################################################
# Constants
###############################################################################

WEEKDAY_NAMES = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                 'Saturday', 'Sunday')

ABBREVIATED_WEEKDAY_NAMES = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

MONTH_NAMES = ('January', 'February', 'March', 'April', 'May', 'June', 'July'
               'August', 'September', 'October', 'November', 'December')

ABBREVIATED_MONTH_NAMES = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'
                           'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

# January 1, 2000 was a saturday.
JAN_1_2000_DAY_NUM = 5

ABBREV_MONTH_NUM_DAYS_PAIRS = (
    ('Jan', 31),
    ('Feb', 28),
    ('Mar', 31),
    ('Apr', 30),
    ('May', 31),
    ('Jun', 30),
    ('Jul', 31),
    ('Aug', 31),
    ('Sep', 30),
    ('Oct', 31),
    ('Nov', 30),
    ('Dec', 31),
)

NOT_IMPLEMENTED = None

class DIRECTIVES:
    ABBREV_WEEKDAY_NAME = 'a'
    WEEKDAY_NAME = 'A'
    ABBREV_MONTH_NAME = 'b'
    MONTH_NAME = 'B'
    LOCALE_DATETIME = 'c'
    DAY_OF_MONTH = 'd'
    HOUR_24 = 'H'
    HOUR_12 = 'I'
    DAY_OF_YEAR = 'j'
    MONTH = 'm'
    MINUTE = 'M'
    AM_PM = 'p'
    SECOND = 'S'
    WEEK_OF_YEAR_SUNDAY = 'U'
    DAY_OF_WEEK = 'w'
    WEEK_OF_YEAR_MONDAY = 'W'
    LOCALE_DATE = 'x'
    LOCALE_TIME = 'X'
    YEAR_NO_CENTURY = 'y'
    YEAR = 'Y'
    TIME_ZONE_OFFSET = 'z'
    TIME_ZONE = 'Z'
    PERCENT = '%'

class STRUCT_TIME:
    TM_YEAR = 'tm_year'
    TM_MON = 'tm_mon'
    TM_MDAY = 'tm_mday'
    TM_HOUR = 'tm_hour'
    TM_MIN = 'tm_min'
    TM_SEC = 'tm_sec'
    TM_WDAY = 'tm_wday'
    TM_YDAY = 'tm_yday'

STRUCT_TIME_FIELDS = (
    'tm_year',
    'tm_mon',
    'tm_mday',
    'tm_hour',
    'tm_min',
    'tm_sec',
    'tm_wday',
    'tm_yday'
)

###############################################################################
# Types
###############################################################################

struct_time = namedtuple('struct_time', STRUCT_TIME_FIELDS)

def time_delta(**kwargs):
    if any(k not in STRUCT_TIME_FIELDS for k in kwargs):
        raise AssertionError
    return struct_time(*[kwargs.get(k, 0) for k in STRUCT_TIME_FIELDS])

###############################################################################
# Date Helpers
###############################################################################

is_leap_year = lambda year: \
    year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

days_in_month = lambda year, month: (
    29 if month == 2 and is_leap_year(year)
    else ABBREV_MONTH_NUM_DAYS_PAIRS[month - 1][1]
)

days_in_year = lambda year: 366 if is_leap_year(year) else 365

is_valid_month_day = lambda year, month, day: day <= days_in_month(year, month)

def date_to_day_of_year(year, month, day):
    """Return the day of year for the specified date in the range 1 - 366.
    """
    # If month is January, just return the day.
    if month == 1:
        return day
    # Accumulate days from all months prior to the specified month.
    num_days = 0
    for i in range(1, month):
        num_days += ABBREV_MONTH_NUM_DAYS_PAIRS[i - 1][1]
    # Maybe add a leap day.
    if month > 2 and is_leap_year(year):
        num_days += 1
    # Return the sum of day and prior months' days.
    return num_days + day

def date_to_day_of_week(year, month, day):
    """Return the day number for the specified date.
    """
    # Calculate the day offset from Jan, 1 in the specified year.
    day_num = date_to_day_of_year(year, month, day)

    is_pre_2k = year < 2000
    if is_pre_2k:
        # Calculate the number of days from the end of the year.
        num_days = days_in_year(year) - day_num + 1
        start, step = 1999, -1
    else:
        # Calculate the number of days from the beginning of the year.
        num_days = day_num - 1
        start, step = 2000, 1

    for _year in range(start, year, step):
        num_days += days_in_year(_year)

    # Add the number of days to the day number for Jan 1, 2000 modulus 7
    # to get the current day number.
    if is_pre_2k:
        num_days = -num_days

    return (JAN_1_2000_DAY_NUM + num_days) % 7

###############################################################################
# struct_time Helpers
###############################################################################

def struct_time_replace(_struct_time, **kwargs):
    if any(k not in STRUCT_TIME_FIELDS for k in kwargs):
        raise AssertionError
    return struct_time(
        *[kwargs.get(k, getattr(_struct_time, k)) for k in STRUCT_TIME_FIELDS]
    )

def add_struct_time_time_delta(_struct_time, _time_delta):
    # Return the result of adding a time_delta to a struct_time.
    # Check that time_delta doesn't specify tm_wday or tm_yday.
    if (_time_delta.tm_wday != 0 or _time_delta.tm_yday != 0):
        raise NotImplementedError
    # Sum seconds.
    seconds = _struct_time.tm_sec + _time_delta.tm_sec
    minutes = 0
    if seconds < 0:
        minutes -= int(-seconds / 60) + 1
        seconds = seconds % 60
    elif seconds > 59:
        minutes += int(seconds / 60)
        seconds = seconds % 60
    # Sum minutes.
    minutes += _struct_time.tm_min + _time_delta.tm_min
    hours = 0
    if minutes < 0:
        hours -= int(-minutes / 60) + 1
        minutes = minutes % 60
    elif minutes > 59:
        hours += int(minutes / 60)
        minutes = minutes % 60
    # Sum hours.
    hours += _struct_time.tm_hour + _time_delta.tm_hour
    day = 0
    if hours < 0:
        day -= int(-hours / 24) + 1
        hours = hours % 24
    elif hours > 23:
        day += int(hours / 24)
        hours = hours % 24
    # Sum days.
    day += _struct_time.tm_mday + _time_delta.tm_mday
    month = 0
    if day < 1:
        month -= int(-day / 32) + 1
        day = 31 - (-day % 32)
    elif day > 31:
        month += int(day / 32)
        day = day % 32
    # Sum months.
    month += _struct_time.tm_mon + _time_delta.tm_mon
    year = 0
    if month < 1:
        year -= int(month / 13) + 1
        month = 12 - (-month % 13)
    elif month > 12:
        year += int(month / 13)
        month = month % 13
    # Sum years.
    year += _struct_time.tm_year + _time_delta.tm_year
    # Increment month if day exceeds max.
    last_day = days_in_month(year, month)
    if day > last_day:
        month += int(day % last_day + 1)
        day = day % last_day + 1
    if month > 12:
        year += int(month / 13)
        month = month % 13
    # Calc day of week / year and return struct_time.
    dyear = date_to_day_of_year(year, month, day)
    dweek = date_to_day_of_week(year, month, day)
    return struct_time(year, month, day, hours, minutes, seconds, dweek, dyear)

###############################################################################
# Parser
###############################################################################

def match_choice(s, choices):
    # Find the first value in choices that is a prefix of s and return a tuple
    # in the format: ( <choice>, <rest-of-s> ) where <rest-of-s> is
    # s[len(choice):], or return False if no match is found.
    for choice in choices:
        if s.startswith(choice):
            return choice, s[len(choice):]
    return False

def parse_integer(s, _len, _min, _max):
    # Attempt to parse an integer of specified length and range and return a
    # tuple in the format: ( <number>, <rest-of-s> ) where <rest-of-s> is
    # s[_len:], or return False if no match is found.
    if len(s) >= _len:
        num_s = s[:_len]
        if all(c.isdigit() for c in num_s):
            num = int(num_s)
            if _min <= num <= _max:
                return num, s[_len:]
    return False

def parse_time_zone_offset(s):
    # Attempt to parse a positive or negative time zone offset and return a
    # tuple in the format: ( <offset-minutes>, <rest-of-s> ), or return False
    # if no match is found.
    if (len(s) == 6
        and (s[0] == '-' or s[0] == '+')
        and s[1].isdigit()
        and s[2].isdigit()
        and s[3] == ':'
        and s[4].isdigit()
        and s[5].isdigit()):
        return int(s[:3]) * 60 + int(s[4:6]), s[6:]
    return False

choice_parser = lambda choices: lambda s: match_choice(s, choices)

positive_integer_parser = lambda _len, _max, _min=0: lambda s: parse_integer(
    s, _len, _min=_min, _max=_max)

DIRECTIVE_PARSER_MAP = {
    DIRECTIVES.ABBREV_WEEKDAY_NAME: choice_parser(ABBREVIATED_WEEKDAY_NAMES),
    DIRECTIVES.WEEKDAY_NAME: choice_parser(WEEKDAY_NAMES),
    DIRECTIVES.ABBREV_MONTH_NAME: choice_parser(ABBREVIATED_MONTH_NAMES),
    DIRECTIVES.MONTH_NAME: choice_parser(MONTH_NAMES),
    DIRECTIVES.LOCALE_DATETIME: NOT_IMPLEMENTED,
    DIRECTIVES.DAY_OF_MONTH: positive_integer_parser(_len=2, _max=31),
    DIRECTIVES.HOUR_24: positive_integer_parser(_len=2, _max=23),
    DIRECTIVES.HOUR_12: positive_integer_parser(_len=2, _min=1, _max=12),
    DIRECTIVES.DAY_OF_YEAR: positive_integer_parser(_len=3, _max=366),
    DIRECTIVES.MONTH: positive_integer_parser(_len=2, _max=12),
    DIRECTIVES.MINUTE: positive_integer_parser(_len=2, _max=59),
    DIRECTIVES.AM_PM: choice_parser(('AM', 'PM')),
    DIRECTIVES.SECOND: positive_integer_parser(_len=2, _max=59),
    DIRECTIVES.WEEK_OF_YEAR_SUNDAY: NOT_IMPLEMENTED,
    DIRECTIVES.DAY_OF_WEEK: positive_integer_parser(_len=1, _max=6),
    DIRECTIVES.WEEK_OF_YEAR_MONDAY: NOT_IMPLEMENTED,
    DIRECTIVES.LOCALE_DATE: NOT_IMPLEMENTED,
    DIRECTIVES.LOCALE_TIME: NOT_IMPLEMENTED,
    DIRECTIVES.YEAR_NO_CENTURY: positive_integer_parser(_len=2, _max=99),
    DIRECTIVES.YEAR: positive_integer_parser(_len=4, _max=9999),
    DIRECTIVES.TIME_ZONE_OFFSET: parse_time_zone_offset,
    DIRECTIVES.TIME_ZONE: choice_parser(('Z',)),
    DIRECTIVES.PERCENT: lambda s: s.startswith('%') and ('', s[2:]),
}

###############################################################################
# API
###############################################################################

def directive_to_struct_time_item(directive, value):
    """Return the struct_time (<key>, <value>) pair for the given matched
    directive and value.
    """
    if directive == DIRECTIVES.YEAR:
        # Return YEAR as TM_YEAR.
        return STRUCT_TIME.TM_YEAR, value
    elif directive == DIRECTIVES.YEAR_NO_CENTURY:
        # Return YEAR_NO_CENTURY as TM_YEAR.
        # Assume that a two-digit year is relative to the year 2000.
        return STRUCT_TIME.TM_YEAR, value + 2000
    elif directive == DIRECTIVES.MONTH:
        # Return MONTH as TM_MON.
        return STRUCT_TIME.TM_MON, value
    elif directive == DIRECTIVES.ABBREV_MONTH_NAME:
        # Return ABBREV_MONTH_NAME as TM_MON.
        return STRUCT_TIME.TM_MON, ABBREVIATED_MONTH_NAMES.index(value)
    elif directive == DIRECTIVES.MONTH_NAME:
        # Return MONTH_NAME as TM_MON.
        return STRUCT_TIME.TM_MON, MONTH_NAMES.index(value)
    elif directive == DIRECTIVES.DAY_OF_MONTH:
        # Return DAY_OF_MONTH as TM_MDAY
        return STRUCT_TIME.TM_MDAY, value
    elif directive == DIRECTIVES.HOUR_24:
        # Return HOUR_24 as TM_HOUR
        return STRUCT_TIME.TM_HOUR, value
    elif directive == DIRECTIVES.HOUR_12:
        # Return HOUR_12 as 0-based TM_HOUR
        return STRUCT_TIME.TM_HOUR, 0 if value == 12 else value
    elif directive == DIRECTIVES.MINUTE:
        # Return MINUTE as TM_MIN
        return STRUCT_TIME.TM_MIN, value
    elif directive == DIRECTIVES.SECOND:
        # Return SECOND as TM_SEC
        return STRUCT_TIME.TM_SEC, value
    elif directive == DIRECTIVES.DAY_OF_WEEK:
        # Return DAY_OF_WEEK as TM_WDAY
        return STRUCT_TIME.TM_WDAY, value
    elif directive == DIRECTIVES.ABBREV_WEEKDAY_NAME:
        # Return ABBREV_WEEKDAY_NAME as TM_WDAY
        return STRUCT_TIME.TM_WDAY, ABBREVIATED_WEEKDAY_NAMES.index(value)
    elif directive == DIRECTIVES.WEEKDAY_NAME:
        # Return WEEKDAY_NAME as TM_WDAY
        return STRUCT_TIME.TM_WDAY, WEEKDAY_NAMES.index(value)
    elif directive == DIRECTIVES.DAY_OF_YEAR:
        # Return DAY_OF_YEAR as TM_YDAY
        return STRUCT_TIME.TM_YDAY, value
    elif directive == DIRECTIVES.TIME_ZONE:
        # Take no action for TIME_ZONE.
        return None
    elif directive == DIRECTIVES.TIME_ZONE_OFFSET:
        # Return TIME_ZONE_OFFSET as TM_MIN - to be subtracted from any
        # existing minute value to arrive at UTC.
        return STRUCT_TIME.TM_MIN, -value
    elif directive == DIRECTIVES.AM_PM:
        # Return AM_PM as TM_HOUR
        # If value = 'PM' return +12 to update hour value to 24-hour format.
        return STRUCT_TIME.TM_HOUR, 12 if value == 'PM' else 0
    elif directive == DIRECTIVES.PERCENT:
        # Take no action for PERCENT.
        return None
    else:
        raise NotImplementedError(
            'struct_time conversion not defined for directive: {}'
            .format(directive)
        )

def strptime(date_string, format):
    """Attempt to parse the date_string as the specified format and return a
    struct_time tuple, or None if parsing fails.
    """
    i = 0
    format_len = len(format)
    # Iterate through the format string, applying parsers and matching literal
    # chars as appropriate.
    struct_time_d = {}
    while i < format_len:
        c = format[i]
        # If the character is not the start of a directive, attempt to match a
        # literal character.
        if c != '%':
            if date_string[0] != c:
                return None
            date_string = date_string[1:]
        else:
            # Read the next character of the directive, letting an IndexError
            # raise if format is exhausted/malformed.
            i += 1
            directive = format[i]
            # Raise a ValueError just like the built-in datetime.strptime()
            # if the directive is invalid.
            if directive not in DIRECTIVE_PARSER_MAP:
                raise ValueError("{} is a bad directive in format {}".format(
                    repr(directive[1]), repr(directive)))
            # Get the parser.
            parser = DIRECTIVE_PARSER_MAP[directive]
            # Check whether the parser is yet to be implemented.
            if parser is NOT_IMPLEMENTED:
                raise NotImplementedError(
                    'parser not defined for directive: {}'.format(directive)
                )
            # Do the parsing.
            result = parser(date_string)
            # Return None on any parsing failure.
            if result is False:
                return None
            value, date_string = result
            # Convert the directive value to a struct_time item.
            struct_time_item = directive_to_struct_time_item(directive, value)
            if struct_time_item is not None:
                k, v = struct_time_item
                # If the key already exists, accumulate, otherwise set.
                if k in struct_time_d:
                    struct_time_d[k] += v
                else:
                    struct_time_d[k] = v
        i += 1

    # Return None if the date string has not been completely consumed.
    if len(date_string) > 0:
        return None

    # Return None if a +12 hour AM_PM = 'PM' accumulation overflowed a parsed
    # HOUR_24 value.
    if not (0 <= struct_time_d.get(STRUCT_TIME.TM_HOUR, 0) <= 23):
        return None

    # Attempt to get year/month/day for date ops.
    year = struct_time_d.get(STRUCT_TIME.TM_YEAR)
    month = struct_time_d.get(STRUCT_TIME.TM_MON)
    day = struct_time_d.get(STRUCT_TIME.TM_MDAY)
    has_date = year is not None and month is not None and day is not None

    # Return None if the specified day is not valid for the month.
    if has_date and not is_valid_month_day(year, month, day):
        return None

    # Create an initial struct_time object.
    _struct_time = struct_time(
        *[struct_time_d.get(k, 0) for k in STRUCT_TIME_FIELDS]
    )

    if has_date:
        # Check whether accumulated minute value exceeds its max as a result of
        # accumulating a time zone offset, requiring some calendar day math.
        if not 0 <= struct_time_d.get(STRUCT_TIME.TM_MIN, 0) <= 59:
            # Pass _struct_time along with an empty time_delta to
            # add_struct_time_time_delta() to take advantage of its
            # over/underflow logic. Note that add_struct_time_time_delta() will
            # take care of setting the final day of week / year.
            _struct_time = add_struct_time_time_delta(
                _struct_time, time_delta())
        else:
            # Calculate the final day of week / year.
            _struct_time = struct_time_replace(
                _struct_time,
                tm_wday=date_to_day_of_week(year, month, day),
                tm_yday=date_to_day_of_year(year, month, day)
            )

    return _struct_time
