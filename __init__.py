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

TIME_ZONES = ('', 'Z')

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
            if 0 <= num <= _max:
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

positive_integer_parser = \
    lambda _len, _max: lambda s: parse_integer(s, _len, _min=0, _max=_max)

DIRECTIVE_PARSER_MAP = {
    DIRECTIVES.ABBREV_WEEKDAY_NAME: choice_parser(ABBREVIATED_WEEKDAY_NAMES),
    DIRECTIVES.WEEKDAY_NAME: choice_parser(WEEKDAY_NAMES),
    DIRECTIVES.ABBREV_MONTH_NAME: choice_parser(ABBREVIATED_MONTH_NAMES),
    DIRECTIVES.MONTH_NAME: choice_parser(MONTH_NAMES),
    DIRECTIVES.LOCALE_DATETIME: NOT_IMPLEMENTED,
    DIRECTIVES.DAY_OF_MONTH: positive_integer_parser(_len=2, _max=31),
    DIRECTIVES.HOUR_24: positive_integer_parser(_len=2, _max=23),
    DIRECTIVES.HOUR_12: positive_integer_parser(_len=2, _max=12),
    DIRECTIVES.DAY_OF_YEAR: positive_integer_parser(_len=36, _max=366),
    DIRECTIVES.MONTH: positive_integer_parser(_len=2, _max=12),
    DIRECTIVES.MINUTE: positive_integer_parser(_len=2, _max=59),
    DIRECTIVES.AM_PM: choice_parser(('AM', 'PM')),
    DIRECTIVES.SECOND: positive_integer_parser(_len=2, _max=59),
    DIRECTIVES.WEEK_OF_YEAR_SUNDAY: positive_integer_parser(_len=2, _max=53),
    DIRECTIVES.DAY_OF_WEEK: positive_integer_parser(_len=1, _max=6),
    DIRECTIVES.WEEK_OF_YEAR_MONDAY: positive_integer_parser(_len=2, _max=53),
    DIRECTIVES.LOCALE_DATE: NOT_IMPLEMENTED,
    DIRECTIVES.LOCALE_TIME: NOT_IMPLEMENTED,
    DIRECTIVES.YEAR_NO_CENTURY: positive_integer_parser(_len=2, _max=99),
    DIRECTIVES.YEAR: positive_integer_parser(_len=4, _max=9999),
    DIRECTIVES.TIME_ZONE_OFFSET: parse_time_zone_offset,
    DIRECTIVES.TIME_ZONE: choice_parser(TIME_ZONES),
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
        # Return INUTE as TM_MIN
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
    else:
        raise NotImplementedError(directive)

def strptime(date_string, format):
    """Attempt to parse the date_string as the specified format and return a
    struct_time tuple, or None if parsing fails.
    """
    i = 0
    format_len = len(format)
    # Iterate through the format string, applying parsers and matching literal
    # chars as appropriate.
    struct_time_d = {}
    utc_offset_minutes = None
    am_pm = None
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
                raise NotImplementedError(directive)
            # Do the parsing.
            result = parser(date_string)
            # Return None on any parsing failure.
            if result is False:
                return None
            value, date_string = result
            # Apply the directive value.
            if directive == DIRECTIVES.TIME_ZONE:
                if value == 'Z':
                    # Time is UTC.
                    utc_offset_minutes = 0
            elif directive == DIRECTIVES.TIME_ZONE_OFFSET:
                # Save the offset.
                utc_offset_minutes = value
            elif directive == DIRECTIVES.AM_PM:
                am_pm = value
            else:
                # Convert the directive value to a struct_time item.
                k, v = directive_to_struct_time_item(directive, value)
                struct_time_d[k] = v
        i += 1

    # Update hour value to 24-hour format if am_pm = 'PM'.
    if am_pm == 'PM':
        struct_time_d['tm_hour'] += 12

    # Apply any time zone offset to result in UTC.
    if utc_offset_minutes is not None and utc_offset_minutes != 0:
        # TODO - do some datetime math.
        raise NotImplementedError

    # Return a struct_time object.
    return struct_time(*[struct_time_d.get(k, 0) for k in struct_time._fields])
