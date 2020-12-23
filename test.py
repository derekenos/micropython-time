
from __init__ import (
    JAN_1_2000_DAY_NUM,
    date_to_day_of_year,
    date_to_day_num,
    is_leap_year,
    strptime,
    struct_time,
)

from testy import (
    Skip,
    assertEqual,
    assertNone,
    assertRaises,
    cli,
)

###############################################################################
# Test date_to_day_of_year()
###############################################################################

def test_date_to_day_of_year_jan_1_2000():
    assertEqual(
        date_to_day_of_year(2000, 1, 1),
        1
    )

def test_date_to_day_of_year():
    assertEqual(
        date_to_day_of_year(2020, 12, 23),
        358
    )

###############################################################################
# Test date_to_day_num()
###############################################################################

def test_is_leap_year():
    for a, b in (
            (1796, True),
            (1800, False),
            (1900, False),
            (2000, True),
            (2100, False),
            (2200, False),
            (2300, False),
            (2400, True),
            (2500, False),
        ):
        assertEqual(is_leap_year(a), b)

def test_date_to_day_num_jan_1_1999_thru_1990():
    for year, day_num in (
            (1999, (JAN_1_2000_DAY_NUM - 365) % 7),
            (1998, (JAN_1_2000_DAY_NUM - 365 * 2) % 7),
            (1997, (JAN_1_2000_DAY_NUM - 365 * 3) % 7),
            (1996, (JAN_1_2000_DAY_NUM - 365 * 3 - 366) % 7),
            (1995, (JAN_1_2000_DAY_NUM - 365 * 4 - 366) % 7),
            (1994, (JAN_1_2000_DAY_NUM - 365 * 5 - 366) % 7),
            (1993, (JAN_1_2000_DAY_NUM - 365 * 6 - 366) % 7),
            (1992, (JAN_1_2000_DAY_NUM - 365 * 6 - 366 * 2) % 7),
            (1991, (JAN_1_2000_DAY_NUM - 365 * 7 - 366 * 2) % 7),
            (1990, (JAN_1_2000_DAY_NUM - 365 * 8 - 366 * 2) % 7),
        ):
        assertEqual(date_to_day_num(year, 1, 1), day_num)

def test_date_to_day_num_jan_1_2000_thru_2009():
    for year, day_num in (
            (2000, JAN_1_2000_DAY_NUM),
            (2001, (JAN_1_2000_DAY_NUM + 366) % 7),
            (2002, (JAN_1_2000_DAY_NUM + 366 + 365) % 7),
            (2003, (JAN_1_2000_DAY_NUM + 366 + 365 * 2) % 7),
            (2004, (JAN_1_2000_DAY_NUM + 366 + 365 * 3) % 7),
            (2005, (JAN_1_2000_DAY_NUM + 366 * 2 + 365 * 3) % 7),
            (2006, (JAN_1_2000_DAY_NUM + 366 * 2 + 365 * 4) % 7),
            (2007, (JAN_1_2000_DAY_NUM + 366 * 2 + 365 * 5) % 7),
            (2008, (JAN_1_2000_DAY_NUM + 366 * 2 + 365 * 6) % 7),
            (2009, (JAN_1_2000_DAY_NUM + 366 * 3 + 365 * 6) % 7),
        ):
        assertEqual(date_to_day_num(year, 1, 1), day_num)

def test_date_to_day_num_spot_check():
    for year, day_num in (
            (1601, 4),
            (1900, 1),
            (1932, 2),
            (1937, 5),
            (1980, 2),
            (1991, 2),
            (2000, 6),
            (2005, 6),
            (2006, 0),
        ):
        print(year)
        assertEqual(date_to_day_num(year, 1, 1), day_num)


def test_date_to_day_num_jan_1_2001():
    assertEqual(
        date_to_day_num(2001, 1, 1),
        (JAN_1_2000_DAY_NUM + 366) % 7
    )

def test_date_to_day_num():
    assertEqual(
        date_to_day_num(2020, 12, 23),
        3
    )

###############################################################################
# Test strptime()
###############################################################################

# Test individual directives.

def test_weekday_name_directive():
    # Test valid values.
    for i, name in enumerate((
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday'
        )):
        assertEqual(
            strptime(name, '%A'),
            struct_time(0, 0, 0, 0, 0, 0, i, 0)
        )
    # Test an invalid value.
    assertNone(strptime('Frunday', '%A'))

def test_abbrev_weekday_name_directive():
    # Test valid values.
    for i, name in enumerate((
            'Sun',
            'Mon',
            'Tue',
            'Wed',
            'Thu',
            'Fri',
            'Sat'
        )):
        assertEqual(
            strptime(name, '%a'),
            struct_time(0, 0, 0, 0, 0, 0, i, 0)
        )
    # Test an invalid value.
    assertNone(strptime('Sunday', '%a'))

def test_abbrev_month_name_directive():
    # Test valid values.
    for i, name in enumerate((
            'Jan',
            'Feb',
            'Mar',
            'Apr',
            'May',
            'Jun',
            'Jul'
            'Aug',
            'Sep',
            'Oct',
            'Nov',
            'Dec'
        )):
        assertEqual(
            strptime(name, '%b'),
            struct_time(0, i, 0, 0, 0, 0, 0, 0)
        )
    # Test an invalid value.
    assertNone(strptime('January', '%b'))

def test_month_name_directive():
    # Test valid values.
    for i, name in enumerate((
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July'
            'August',
            'September',
            'October',
            'November',
            'December'
        )):
        assertEqual(
            strptime(f'{name}', '%B'),
            struct_time(0, i, 0, 0, 0, 0, 0, 0)
        )
    # Test an invalid value.
    assertNone(strptime('Jan', '%B'))

def test_locale_datetime_directive_not_implemented():
    # Test that locale datetime is not implemented.
    assertRaises(NotImplementedError, strptime, '', '%c')

def test_day_of_month_directive():
    # Test valid values.
    for i in range(32):
        assertEqual(
            strptime(f'{i:02}', '%d'),
            struct_time(0, 0, i, 0, 0, 0, 0, 0)
        )
    # Test an invalid value.
    assertNone(strptime('32', '%d'))

def test_hour_24_directive():
    # Test valid values.
    for i in range(24):
        assertEqual(
            strptime(f'{i:02}', '%H'),
            struct_time(0, 0, 0, i, 0, 0, 0, 0)
        )
    # Test an invalid value.
    assertNone(strptime('24', '%H'))

def test_hour_12_directive():
    # Test valid values.
    for i in range(1, 13):
        assertEqual(
            strptime(f'{i:02}', '%I'),
            struct_time(0, 0, 0, i, 0, 0, 0, 0)
        )
    # Test an invalid value.
    assertNone(strptime('00', '%I'))

def test_day_of_year_directive():
    # Test valid values.
    for i in range(367):
        assertEqual(
            strptime(f'{i:03}', '%j'),
            struct_time(0, 0, 0, 0, 0, 0, 0, i)
        )
    # Test an invalid value.
    assertNone(strptime('367', '%j'))

def test_month_directive():
    # Test valid values.
    for i in range(13):
        assertEqual(
            strptime(f'{i:02}', '%m'),
            struct_time(0, i, 0, 0, 0, 0, 0, 0)
        )
    # Test an invalid value.
    assertNone(strptime('13', '%m'))

def test_minute_directive():
    # Test valid values.
    for i in range(60):
        assertEqual(
            strptime(f'{i:02}', '%M'),
            struct_time(0, 0, 0, 0, i, 0, 0, 0)
        )
    # Test an invalid value.
    assertNone(strptime('60', '%M'))

def test_am_pm_directive():
    # Test AM.
    assertEqual(
        strptime(f'AM', '%p'),
        struct_time(0, 0, 0, 0, 0, 0, 0, 0)
    )
    # Test PM.
    assertEqual(
        strptime(f'PM', '%p'),
        struct_time(0, 0, 0, 12, 0, 0, 0, 0)
    )
    # Test an invalid value.
    assertNone(strptime('AA', '%p'))

def test_second_directive():
    # Test valid values.
    for i in range(60):
        assertEqual(
            strptime(f'{i:02}', '%S'),
            struct_time(0, 0, 0, 0, 0, i, 0, 0)
        )
    # Test an invalid value.
    assertNone(strptime('60', '%S'))

def test_week_of_year_sunday_directive_not_implemented():
    # Test that week_of_year_sunday is not implemented.
    assertRaises(NotImplementedError, strptime, '', '%U')

def test_day_of_week_directive():
    # Test valid values.
    for i in range(7):
        assertEqual(
            strptime(f'{i}', '%w'),
            struct_time(0, 0, 0, 0, 0, 0, i, 0)
        )
    # Test an invalid value.
    assertNone(strptime('7', '%w'))

def test_week_of_year_monday_directive_not_implemented():
    # Test that week_of_year_monday is not implemented.
    assertRaises(NotImplementedError, strptime, '', '%W')

def test_locale_date_directive_not_implemented():
    # Test that locale_date is not implemented.
    assertRaises(NotImplementedError, strptime, '', '%x')

def test_locale_time_directive_not_implemented():
    # Test that locale_time is not implemented.
    assertRaises(NotImplementedError, strptime, '', '%X')

def test_year_no_century_directive():
    # Test valid values.
    for i in range(100):
        assertEqual(
            strptime(f'{i:02}', '%y'),
            struct_time(2000 + i, 0, 0, 0, 0, 0, 0, 0)
        )
    # Test an invalid value.
    assertNone(strptime('100', '%y'))

def test_year_directive():
    # Test valid values.
    for i in range(10000):
        assertEqual(
            strptime(f'{i:04}', '%Y'),
            struct_time(i, 0, 0, 0, 0, 0, 0, 0)
        )
    # Test an invalid value.
    assertNone(strptime('10000', '%Y'))

def test_time_zone_offset_directive():
    # Test valid values.
    for offset_str, offset_mins in (
            ('+00:00', 0),
            ('-00:00', 0),
            ('+01:00', 60),
            ('-01:00', -60),
            ('+12:00', 720),
        ):
        assertEqual(
            strptime(offset_str, '%z'),
            struct_time(0, 0, 0, 0, offset_mins, 0, 0, 0)
        )
    # Test an invalid value.
    assertNone(strptime('00:00', '%z'))

def test_time_zone_directive():
    # Test the only valid value.
    assertEqual(
        strptime('Z', '%Z'),
        struct_time(0, 0, 0, 0, 0, 0, 0, 0)
    )
    # Test an invalid value.
    assertNone(strptime('z', '%Z'))

def test_percent_directive():
    # Test the only valid value.
    assertEqual(
        strptime('%', '%%'),
        struct_time(0, 0, 0, 0, 0, 0, 0, 0)
    )
    # Test an invalid value.
    assertNone(strptime('!', '%%'))

# Test multiple directives.

def test_iso8601_date():
    assertEqual(
        strptime('2020-12-23', '%Y-%m-%d'),
        struct_time(2020, 12, 23, 0, 0, 0, 0, 0)
    )

def test_iso8601_datetime_utc_offset():
    assertEqual(
        strptime('2020-12-23T01:01:20+00:00', '%Y-%m-%dT%H:%M:%S%z'),
        struct_time(2020, 12, 23, 1, 1, 20, 0, 0)
    )

def test_iso8601_datetime_with_nonzero_utc_offset():
    raise Skip
    assertEqual(
        strptime('2020-12-23T01:01:20+05:00', '%Y-%m-%dT%H:%M:%S%z'),
        struct_time(2020, 12, 23, 1, 1, 20, 0, 0)
    )

def test_iso8601_datetime_utc_timezone():
    assertEqual(
        strptime('2020-12-23T01:01:20Z', '%Y-%m-%dT%H:%M:%S%Z'),
        struct_time(2020, 12, 23, 1, 1, 20, 0, 0)
    )

def test_iso8601_datetime_utc_timezone_no_delimiters():
    assertEqual(
        strptime('20201223T010120Z', '%Y%m%dT%H%M%S%Z'),
        struct_time(2020, 12, 23, 1, 1, 20, 0, 0)
    )

def test_am_time():
    assertEqual(
        strptime('08:10AM', '%H:%M%p'),
        struct_time(0, 0, 0, 8, 10, 0, 0, 0)
    )

def test_pm_time():
    assertEqual(
        strptime('08:10PM', '%H:%M%p'),
        struct_time(0, 0, 0, 20, 10, 0, 0, 0)
    )

def test_pm_time_overflow():
    assertNone(strptime('12:10PM', '%H:%M%p'))


# Test things that are not yet implemented.

def test_invalid_day_of_month():
    # i.e. February 30
    raise Skip


if __name__ == '__main__':
    cli(globals())
