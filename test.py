
from __init__ import (
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
    for i in range(13):
        assertEqual(
            strptime(f'{i:02}', '%I'),
            struct_time(0, 0, 0, i, 0, 0, 0, 0)
        )
    # Test an invalid value.
    assertNone(strptime('13', '%I'))

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
