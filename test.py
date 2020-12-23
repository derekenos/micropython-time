
from __init__ import (
    strptime,
    struct_time,
)

from testy import (
    Skip,
    assertEqual,
    cli,
)


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


if __name__ == '__main__':
    cli(globals())
