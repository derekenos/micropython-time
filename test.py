
from __init__ import (
    ABBREV_MONTH_NUM_DAYS_PAIRS,
    JAN_1_2000_DAY_NUM,
    date_to_day_of_year,
    date_to_day_of_week,
    is_leap_year,
    strptime,
    struct_time,
    add_struct_time_time_delta,
    time_delta,
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

_days_in_months = lambda n: sum(x[1] for x in ABBREV_MONTH_NUM_DAYS_PAIRS[:n])

def test_date_to_day_of_year():
    for year, month, day, day_of_year in (
            (1995, 1, 10, _days_in_months(0) + 10 + 0),
            (1996, 2, 11, _days_in_months(1) + 11 + 0), # no leap day yet
            (1997, 3, 12, _days_in_months(2) + 12 + 0),
            (1998, 4, 13, _days_in_months(3) + 13 + 0),
            (1999, 5, 14, _days_in_months(4) + 14 + 0),
            (2000, 6, 15, _days_in_months(5) + 15 + 1),
            (2001, 7, 16, _days_in_months(6) + 16 + 0),
            (2002, 8, 17, _days_in_months(7) + 17 + 0),
            (2003, 9, 18, _days_in_months(8) + 18 + 0),
            (2004, 10, 19, _days_in_months(9) + 19 + 1),
            (2005, 11, 20, _days_in_months(10) + 20 + 0),
            (2006, 12, 21, _days_in_months(11) + 21 + 0),
        ):
        assertEqual(date_to_day_of_year(year, month, day), day_of_year)

###############################################################################
# Test date_to_day_of_week()
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

def test_date_to_day_of_week_jan_1_1999_thru_1990():
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
        assertEqual(date_to_day_of_week(year, 1, 1), day_num)

def test_date_to_day_of_week_jan_1_2000_thru_2009():
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
        assertEqual(date_to_day_of_week(year, 1, 1), day_num)

def test_date_to_day_of_week_spot_check():
    for year, month, day, day_num in (
            (1601, 1, 1, 1),
            (1800, 1, 1, 3),
            (1800, 12, 31, 3),
            (1801, 1, 1, 4),
            (1801, 12, 31, 4),
            (1834, 1, 1, 3),
            (1834, 12, 31, 3),
            (1900, 1, 1, 1),
            (1900, 6, 15, 5),
            (1932, 1, 1, 5),
            (1932, 6, 15, 3),
            (1937, 1, 1, 5),
            (1937, 6, 15, 2),
            (1954, 1, 1, 5),
            (1954, 6, 15, 2),
            (1972, 1, 1, 6),
            (1972, 6, 15, 4),
            (1980, 1, 1, 2),
            (1980, 6, 15, 0),
            (1991, 1, 1, 2),
            (1991, 6, 15, 6),
            (2000, 1, 1, 6),
            (2000, 6, 15, 4),
            (2005, 1, 1, 6),
            (2005, 6, 15, 3),
            (2005, 12, 31, 6),
            (2006, 1, 1, 0),
            (2006, 6, 15, 4),
            (2006, 12, 31, 0),
            (2029, 1, 1, 1),
            (2029, 6, 15, 5),
            (2029, 12, 31, 1),
            (2121, 1, 1, 3),
            (2121, 6, 15, 0),
            (2121, 12, 31, 3),

        ):
        assertEqual(date_to_day_of_week(year, month, day), day_num)

###############################################################################
# Test add_struct_time_time_delta()
###############################################################################

_assertStructTimeDelta = lambda _struct_time, _time_delta, expected: \
    assertEqual(
        add_struct_time_time_delta(_struct_time, _time_delta),
        expected
    )

def test_add_struct_time_time_delta_zero_delta():
    _assertStructTimeDelta(
        struct_time(2000, 1, 1, 0, 0, 0, 6, 1),
        time_delta(),
        struct_time(2000, 1, 1, 0, 0, 0, 6, 1)
    )

def test_add_struct_time_time_delta_second():
    _assertStructTimeDelta(
        struct_time(2000, 1, 1, 0, 0, 1, 6, 1),
        time_delta(tm_sec=1),
        struct_time(2000, 1, 1, 0, 0, 2, 6, 1)
    )

def test_add_struct_time_time_delta_minute():
    _assertStructTimeDelta(
        struct_time(2000, 1, 1, 0, 1, 0, 6, 1),
        time_delta(tm_min=1),
        struct_time(2000, 1, 1, 0, 2, 0, 6, 1)
    )

def test_add_struct_time_time_delta_hour():
    _assertStructTimeDelta(
        struct_time(2000, 1, 1, 1, 0, 0, 6, 1),
        time_delta(tm_hour=1),
        struct_time(2000, 1, 1, 2, 0, 0, 6, 1)
    )

def test_add_struct_time_time_delta_day():
    _assertStructTimeDelta(
        struct_time(2000, 1, 1, 0, 0, 0, 6, 1),
        time_delta(tm_mday=1),
        struct_time(2000, 1, 2, 0, 0, 0, 0, 2)
    )

def test_add_struct_time_time_delta_second_overflow():
    _assertStructTimeDelta(
        struct_time(2000, 1, 1, 0, 0, 1, 6, 1),
        time_delta(tm_sec=59),
        struct_time(2000, 1, 1, 0, 1, 0, 6, 1),
    )

def test_add_struct_time_time_delta_minute_overflow():
    _assertStructTimeDelta(
        struct_time(2000, 1, 1, 0, 1, 0, 6, 1),
        time_delta(tm_min=59),
        struct_time(2000, 1, 1, 1, 0, 0, 6, 1)
    )

def test_add_struct_time_time_delta_hour_overflow():
    _assertStructTimeDelta(
        struct_time(2000, 1, 1, 1, 0, 0, 6, 1),
        time_delta(tm_hour=23),
        struct_time(2000, 1, 2, 0, 0, 0, 0, 2)

    )

def test_add_struct_time_time_delta_second_underflow():
    _assertStructTimeDelta(
        struct_time(2000, 1, 1, 0, 0, 1, 6, 1),
        time_delta(tm_sec=-2),
        struct_time(1999, 12, 31, 23, 59, 59, 5, 365),
    )

def test_add_struct_time_time_delta_minute_underflow():
    _assertStructTimeDelta(
        struct_time(2000, 1, 1, 0, 1, 0, 6, 1),
        time_delta(tm_min=-2),
        struct_time(1999, 12, 31, 23, 59, 0, 5, 365),
    )

def test_add_struct_time_time_delta_hour_underflow():
    _assertStructTimeDelta(
        struct_time(2000, 1, 1, 1, 0, 0, 6, 1),
        time_delta(tm_hour=-2),
        struct_time(1999, 12, 31, 23, 0, 0, 5, 365),
    )

def test_add_struct_time_time_delta_day_underflow():
    _assertStructTimeDelta(
        struct_time(2000, 1, 1, 0, 0, 0, 6, 1),
        time_delta(tm_mday=-2),
        struct_time(1999, 12, 30, 0, 0, 0, 4, 364),
    )

def test_add_struct_time_time_delta_month_underflow():
    _assertStructTimeDelta(
        struct_time(2000, 1, 1, 0, 0, 0, 6, 1),
        time_delta(tm_mon=-1),
        struct_time(1999, 12, 1, 0, 0, 0, 3, 335),
    )

def test_add_struct_time_time_delta_wday_not_implemented():
    assertRaises(
        NotImplementedError,
        add_struct_time_time_delta,
        struct_time(2000, 1, 1, 0, 0, 0, 6, 1),
        time_delta(tm_wday=1),
    )

def test_add_struct_time_time_delta_yday_not_implemented():
    assertRaises(
        NotImplementedError,
        add_struct_time_time_delta,
        struct_time(2000, 1, 1, 0, 0, 0, 6, 1),
        time_delta(tm_yday=1),
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
            struct_time(0, 0, 0, 0 if i == 12 else i, 0, 0, 0, 0)
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
            ('+01:00', -60),
            ('-01:00', 60),
            ('+12:00', -720),
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
        struct_time(2020, 12, 23, 0, 0, 0, 3, 358)
    )

def test_iso8601_datetime_utc_offset():
    assertEqual(
        strptime('2020-12-23T01:01:20+00:00', '%Y-%m-%dT%H:%M:%S%z'),
        struct_time(2020, 12, 23, 1, 1, 20, 3, 358)
    )

def test_iso8601_datetime_with_nonzero_utc_offset():
    assertEqual(
        strptime('2020-12-23T05:01:20+05:00', '%Y-%m-%dT%H:%M:%S%z'),
        struct_time(2020, 12, 23, 0, 1, 20, 3, 358)
    )

def test_iso8601_datetime_with_nonzero_utc_offset_day_undeflow():
    assertEqual(
        strptime('2020-12-23T04:01:20+05:00', '%Y-%m-%dT%H:%M:%S%z'),
        struct_time(2020, 12, 22, 23, 1, 20, 2, 357)
    )

def test_iso8601_datetime_with_nonzero_utc_offset_day_overflow():
    assertEqual(
        strptime('2020-12-22T23:01:20-05:00', '%Y-%m-%dT%H:%M:%S%z'),
        struct_time(2020, 12, 23, 4, 1, 20, 3, 358)
    )

def test_iso8601_datetime_utc_timezone():
    assertEqual(
        strptime('2020-12-23T01:01:20Z', '%Y-%m-%dT%H:%M:%S%Z'),
        struct_time(2020, 12, 23, 1, 1, 20, 3, 358)
    )

def test_iso8601_datetime_utc_timezone_no_delimiters():
    assertEqual(
        strptime('20201223T010120Z', '%Y%m%dT%H%M%S%Z'),
        struct_time(2020, 12, 23, 1, 1, 20, 3, 358)
    )

def test_am_time():
    assertEqual(
        strptime('08:10AM', '%H:%M%p'),
        struct_time(0, 0, 0, 8, 10, 0, 0, 0)
    )

def test_pm_time_with_hour_12():
    assertEqual(
        strptime('08:10PM', '%I:%M%p'),
        struct_time(0, 0, 0, 20, 10, 0, 0, 0)
    )

def test_noon_pm_time_with_hour_12():
    assertEqual(
        strptime('12:00PM', '%I:%M%p'),
        struct_time(0, 0, 0, 12, 0, 0, 0, 0)
    )

def test_last_day_of_feb_during_leap_year():
    assertEqual(
        strptime('2000-02-29', '%Y-%m-%d'),
        struct_time(2000, 2, 29, 0, 0, 0, 2, 60)
    )


# Test invalid value combinations.

def test_invalid_day_of_month():
    # Test the day after each month's last day ina common year.
    for month in range(1, 13):
        day = ABBREV_MONTH_NUM_DAYS_PAIRS[month - 1][1] + 1
        assertNone(strptime(f'2001-{month:02}-{day:02}', '%Y-%m-%d'))

    # Test day after last day of Feb during a leap year.
    assertNone(strptime('2000-02-30', '%Y-%m-%d'))


# Test illogical directive combinations.

def test_valid_hour_24_specified_as_pm():
    assertEqual(
        strptime('08:10PM', '%H:%M%p'),
        struct_time(0, 0, 0, 20, 10, 0, 0, 0)
    )

def test_invalid_hour_24_specified_as_pm():
    assertNone(strptime('20:10PM', '%H:%M%p'))


if __name__ == '__main__':
    cli(globals())
