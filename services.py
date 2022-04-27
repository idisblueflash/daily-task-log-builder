import calendar
from datetime import timedelta
from typing import List

from dateutil.parser import parse


class DailyLogRow:
    def __init__(self, row, date):
        self.row = row
        self.start_time = None
        self.description = None
        self.status = 'DONE'
        self.date = self._parse_date(date)
        self.day = None

    def parse(self):
        columns = self.row.split(',')
        persons = None
        start_time = None
        description = None

        if len(columns) == 3:
            start_time, description, persons = columns
        if len(columns) == 2:
            start_time, description = columns
        start_time = start_time.strip()
        hour, minute = start_time.split(':')
        self.start_time = timedelta(hours=int(hour), minutes=int(minute))

        self.description = description.strip()

        self.day = calendar.day_abbr[self.date.weekday()]

    @classmethod
    def _get_category(cls, description):
        mapping = {
            'investigat': 'Investigation',
            'meet': 'Communication',
            'communicat': 'Communication',
            'discus': 'Discussion',
            'pair': 'Pairing',
            'daily': 'Daily Works'
        }  # the order of key-value matters, the higher the first selected out

        for key, value in mapping.items():
            if key in description.lower():
                return value

    def _parse_date(self, date):
        return parse(date)


class DailyLog:
    def __init__(self, date: str, rows: List[str]):
        self.date = date
        self.rows = rows
