import datetime as dt
import dateutil.parser as dtp
import pytz
import unittest
import calendar


class DTHelperError(Exception):
    pass


class DatetimeHelper:

    @classmethod
    def now_utc(cls, tz=pytz.utc):
        now = dt.datetime.utcnow()
        now = now.replace(tzinfo=tz)
        return now

    @classmethod
    def to_str(cls, datetime):
        if datetime is None:
            return None
        # order is important - a datetime is a date but a date is not a datetime
        if isinstance(datetime, dt.datetime):
            dt_str = datetime.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(datetime, dt.date):
            dt_str = datetime.strftime("%Y-%m-%d")
        else:
            raise DTHelperError(
                F'datetime argument is of type {str(type(datetime))}, not date or datetime')
        return dt_str

    @classmethod
    def to_json(cls, value):
        if value is None:
            return None
        # order is important - a datetime is a date but a date is not a datetime
        if isinstance(value, dt.datetime):
            dtj = value.isoformat()
        elif isinstance(value, dt.date):
            dtj = value.isoformat()
        elif isinstance(value, dt.time):
            dtj = value.isoformat()
        else:
            raise DTHelperError(
                F'Argument is of type {str(type(value))}, not date, time or datetime')
        return dtj

    @classmethod
    def dt_from_string(cls, dt_str: str, tz=pytz.utc):
        if dt_str is None:
            return None
        datetime = dtp.parse(dt_str)
        udatetime = cls.add_tz(datetime, tz=tz)
        return udatetime

    @classmethod
    def from_timestamp(cls, timestamp, tz=None):
        if timestamp is None:
            return None
        dtv = dt.datetime.utcfromtimestamp(timestamp)
        if tz:
            dtv = cls.add_tz(dtv, tz=tz)
        return dtv

    @classmethod
    def from_qb_timestamp(cls, timestamp: str):
        if timestamp is None:
            return None
        assert isinstance(
            timestamp, str), F'String expected; not: {str(timestamp)}'

        datetime = dt.datetime.utcfromtimestamp(int(timestamp) / float(1000))
        return datetime

    @classmethod
    def add_tz(cls, datetime: dt.datetime, tz=pytz.utc):
        udatetime = datetime.replace(tzinfo=tz)
        return udatetime

    @classmethod
    def utc2local(cls, datetime, local_tz=pytz.timezone("US/Pacific")):
        local_dt = datetime.astimezone(
            local_tz).strftime('%m-%d-%Y %I:%M %p%z')
        return local_dt

    @classmethod
    def dstr_from_dtstr(cls, dt_str: str, tz=pytz.utc):
        dtm = cls.dt_from_string(dt_str, tz)
        date = cls.date_from_dt(dtm)
        date = cls.to_str(date)
        return date

    @classmethod
    def tz_from_dtstr(cls, dt_str: str, tz=pytz.utc):
        dtm = cls.dt_from_string(dt_str, tz)
        date_time = dtm.strftime("%Y-%m-%dT%H:%M:%S")
        return date_time

    @classmethod
    def date_from_timestamp(cls,  timestamp: int, tz=pytz.utc):
        dtv = cls.from_timestamp(timestamp, tz=tz)
        return cls.date_from_dt(dtv)

    @classmethod
    def date_from_dt(cls, datetime: dt.datetime):
        return datetime.date() if datetime else None

    @classmethod
    def dt_from_date(cls, datev: dt.date):
        if datev is None:
            return None
        dtv = dt.datetime(datev.year, datev.month, datev.day)
        return dtv

    @classmethod
    def date_difference(cls, dt1, dt2):
        dt_diff: dt.timedelta = dt1 - dt2
        days_diff = dt_diff.days
        return abs(days_diff)

    @classmethod
    def date_from_tz_timestamp(cls, timestamp: int):
        datetime = dt.datetime.utcfromtimestamp(timestamp / float(1000))
        return datetime

    @classmethod
    def add_months(cls, date, months):
        date = cls.dt_from_string(date)
        month = date.month - 1 + months
        year = date.year + month // 12
        month = month % 12 + 1
        day = min(date.day, calendar.monthrange(year, month)[1])
        added_dt = dt.date(year, month, day)
        return cls.to_str(added_dt)


class DTHelperTests(unittest.TestCase):

    def test_to_str(self):
        dtv = DatetimeHelper.dt_from_string('10/30/2019 15:30')
        sdt = DatetimeHelper.to_str(dtv)
        dav = dtv.date()
        sda = DatetimeHelper.to_str(dav)

        self.assertEqual(sdt, '2019-10-30 15:30:00')
        self.assertEqual(sda, '2019-10-30')

    def test_days_diff(self):
        dtv1 = DatetimeHelper.dt_from_string('10/15/2019 15:30')
        dtv2 = DatetimeHelper.dt_from_string('10/30/2019 15:30')
        days_diff = DatetimeHelper.date_difference(dtv1, dtv2)

        self.assertEqual(0, 0)

    def test_dt_str(self):
        dtv1 = DatetimeHelper.dt_from_string('01/20/2021T06:36:38.421258Z')
        self.assertEqual(0, 0)