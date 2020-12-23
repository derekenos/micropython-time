"""
See: https://docs.python.org/3/library/time.html#time.strftime
"""

from collections import namedtuple

###############################################################################
# Constants
###############################################################################

WEEKDAY_NAMES = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                 'Friday', 'Saturday')

ABBREVIATED_WEEKDAY_NAMES = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')

MONTH_NAMES = ('January', 'February', 'March', 'April', 'May', 'June', 'July'
               'August', 'September', 'October', 'November', 'December')

ABBREVIATED_MONTH_NAMES = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'
                           'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

# January 1, 2000 was a saturday.
JAN_1_2000_DAY_NUM = 6

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

###############################################################################
# Types
###############################################################################

struct_time = namedtuple('struct_time', (
    'tm_year',
    'tm_mon',
    'tm_mday',
    'tm_hour',
    'tm_min',
    'tm_sec',
    'tm_wday',
    'tm_yday'
))

###############################################################################
# Date Helpers
###############################################################################

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

days_in_year = lambda year: 366 if is_leap_year(year) else 365

def date_to_day_of_year(year, month, day):
    """Return the day of year for the specified date in the range 1 - 366.
    Note that arguments are expected to be 1-based because 0-based hurts my
    brain.
    """
    if month == 0 or day == 0:
        raise AssertionError('Please specify 1-based values')
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

def date_to_day_num(year, month, day):
    """Return the day number for the specified date.
    Note that arguments are expected to be 1-based because 0-based hurts my
    brain.
    """
    if month == 0 or day == 0:
        raise AssertionError('Please specify 1-based values')

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
        # Return HOUR_12 as TM_HOUR
        # We don't have the am/pm context here so can't do any conversion.
        return STRUCT_TIME.TM_HOUR, value
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
        # Return TIME_ZONE_OFFSET as TM_MIN - to be added to any existing
        # minute value.
        return STRUCT_TIME.TM_MIN, value
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

    # Check whether accumulated minute value exceeds its max as a result of
    # accumulating a time zone offset, requiring some calendar day math.
    if not 0 <= struct_time_d.get(STRUCT_TIME.TM_MIN, 0) <= 59:
        raise NotImplementedError('todo - calendar math')

    # Return a struct_time object.
    return struct_time(*[struct_time_d.get(k, 0) for k in struct_time._fields])
