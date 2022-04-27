import calendar
from datetime import timedelta
from typing import List

from dateutil.parser import parse
from tabulate import tabulate


class DailyLogRow:
    person = None

    def __init__(self, row, date):
        self.priority = None
        self.category = None
        self.row = row
        self.start_time = None
        self.end_time = None
        self.description = None
        self.status = 'DONE'
        self.date = self._parse_date(date)
        self.day = None

    def parse(self):
        columns = self.row.split(',')
        persons = ''
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
        self.persons = self._get_person(persons)
        self.category = self._get_category(self.description)
        self.priority = self._get_priority(self.description)

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

    def _get_duration(self):
        if self.end_time is None:
            return 0

        duration = self.end_time - self.start_time
        return round(duration.seconds / 3600, 2)

    def _get_person(self, persons: str):
        persons = persons.strip()
        if persons == '':
            return self.person
        people = f'{self.person} {persons}'.split(' ')
        return ', '.join(people)

    def _get_time(self):
        if self.end_time is None:
            return f'{self._get_simple_time(self.start_time)} - ?'

        return f'{self._get_simple_time(self.start_time)} - {self._get_simple_time(self.end_time)}'

    @staticmethod
    def _get_simple_time(time: timedelta) -> str:
        digits = str(time).split(':')
        return ':'.join(digits[:2])

    @classmethod
    def _get_priority(cls, description):
        raise NotImplementedError


class FlashDailyLogRow(DailyLogRow):
    person = 'Flash'

    @classmethod
    def _get_priority(cls, description):
        mapping = {
            'ai recom': 'High',
            'devops': 'Medium',
            'daily': 'Low',
            'break': 'Low'
        }

        for key, value in mapping.items():
            if key in description.lower():
                return value
        return 'Medium'


class DailyLog:
    log_class = None

    def __init__(self, date: str, rows: List[str]):
        self.date = date
        self.rows = rows
        self.logs = []

    def handle(self):
        past_log = None
        for row in self.rows:
            current_log = self.log_class(row, self.date)
            current_log.parse()
            if past_log:
                past_log.end_time = current_log.start_time
            past_log = current_log
            self.logs.append(past_log)

    def report(self):
        headers = ['Date', 'Day', 'Persons Involved',
                   'Time', 'Category', 'Priority', 'Description',
                   'Estimate Hours', 'Total Hours', 'Status']
        table = [[log.date, log.day, log.persons,
                  log._get_time(), log.category, log.priority, log.description,
                  log._get_duration(), 0, log.status]
                 for log in self.logs]
        print('')
        print(tabulate(table, headers=headers))


class FlashDailyLog(DailyLog):
    log_class = FlashDailyLogRow
