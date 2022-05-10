import os
import json
import calendar
from datetime import timedelta
from typing import List

import spacy
from dateutil.parser import parse
from tabulate import tabulate

from email_services import send_email

with open('configure.json') as f:
    configure = json.load(f)


class BaseDailyLogRow:
    person = configure.get('user_name')

    def __init__(self, row, date):
        self.persons_involved = None
        self.priority = None
        self.category = None
        self.row = row
        self.start_time = None
        self.end_time = None
        self.description = None
        self.status = 'DONE'
        self.date = date
        self.day = None

    def parse(self):
        doc =self._get_nlp_result_doc()
        start_time = self._get_start_time(doc)
        if start_time is None:
            raise Exception(f'None start time found: in {self.row}')
        hour, minute = start_time.split(':')
        self.start_time = timedelta(hours=int(hour), minutes=int(minute))

        self.description = self._get_description(doc)

        self.day = calendar.day_abbr[parse(self.date).weekday()]
        self.persons_involved = self._get_persons_involed(doc)
        self.category = self._get_category(self.description)
        self.priority = self._get_priority(self.description)

    @classmethod
    def _get_category(cls, description):

        for key, value in configure.get('category').items():
            if key in description.lower():
                return value
        return 'Tasks'

    def _parse_date(self, date):
        return parse(date)

    def _get_duration(self):
        if self.end_time is None:
            return 0

        duration = self.end_time - self.start_time
        return round(duration.seconds / 3600, 2)

    def _get_persons_involed(self, doc):
        propns =  [self.person] + [token.text for token in doc if token.pos_ == 'PROPN']

        members = list(set([name for name in propns if name in configure.get('team_members', [])]))

        return ', '.join(sorted(members))

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

    def _get_description(self, doc):
        start_time = self._get_start_time(doc)
        if start_time:
            return doc.text.replace(start_time, '').strip()

    def _get_nlp_result_doc(self):
        nlp = spacy.load('en_core_web_sm')
        return nlp(self.row)

    def _get_start_time(self, doc):
        first_token = doc[0]
        if first_token.tag_ == 'CD' and first_token.pos_ == 'NUM':
            return first_token.text


class DefaultDailyLogRow(BaseDailyLogRow):

    def _get_priority(self, description):
        for key, value in configure.get('priority').items():
            if key in description.lower():
                return value
        return 'Medium'


class DefaultDailyLog:
    log_class = DefaultDailyLogRow

    def __init__(self, date: str, rows: List[str]):
        self.total_hours = 0
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

        self.logs = [log for log in self.logs if log.category != 'Break']

    def _get_total_hours(self, hours):
        self.total_hours += hours
        return self.total_hours

    def _get_table(self):
        return [[log.date, log.day, log.persons_involved,
                 log._get_time(), log.category, log.priority, log.description,
                 log._get_duration(), self._get_total_hours(log._get_duration()), log.status]
                for log in self.logs]

    def report(self):
        headers = ['Date 日期', 'Day', 'Persons Involved',
                   'Time 时间', 'Category 工作列别', 'Priority 重要性', 'Description 内容描述',
                   'Estimate Hours', 'Total Hours', 'Status 完成状态']
        table = self._get_table()
        print('')
        print(tabulate(table, headers=headers))


class LogReader:
    logs = []
    log_class = DefaultDailyLog
    file_name = None
    data = {}
    daily = True

    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        self._parse_file()
        self._parse_logs()

    def _get_lines(self):
        with open(self.file_name, encoding='utf-8') as log_file:
            lines = [line for line in log_file]

        return lines

    def _parse_file(self):
        current_key = None
        for line in self._get_lines():
            if line.startswith('#'):
                current_key = self._initial_log_key(line)
                continue
            if current_key:
                self._add_line_by_key(current_key, line)

    def _initial_log_key(self, line):
        key = self._parse_title(line)
        self.data[key] = []
        return key

    @staticmethod
    def _has_started_with_time(line):
        hour_data = line.split(':')[0]
        return hour_data.isnumeric()

    def _add_line_by_key(self, key, line):
        if self._has_started_with_time(line):
            self.data[key].append(line.strip())
        else:
            if len(self.data[key]) == 0:
                raise Exception(f'Empty list in data {self.data} with key {key}')
            last_line = self.data[key].pop()
            last_line = f'{last_line}\n{line}'
            self.data[key].append(last_line.strip())

    def _parse_title(self, line):
        return line.replace('#', '', 1).strip()

    def _parse_logs(self):
        if self.log_class is None:
            raise Exception('You must assign log_class')

        for key in self.data.keys():
            service = self.log_class(key, self.data[key])
            service.handle()
            self.logs = self.logs + service._get_table()
            if self.daily:
                break

    def _get_headers(self):
        return ['Date 日期', 'Day', 'Persons Involved',
                'Time 时间', 'Category 工作列别', 'Priority 重要性', 'Description 内容描述',
                'Estimate Hours', 'Total Hours', 'Status 完成状态']

    def report(self):
        print(tabulate(self.logs, headers=self._get_headers()))

    def save_excel(self):
        import pandas as pd

        writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
        df = pd.DataFrame(self.logs, columns=self._get_headers())
        df.to_excel(writer, sheet_name='Daily Task Log')
        for column in df:
            column_width = max(df[column].astype(str).map(len).max(), len(column))
            column_index = df.columns.get_loc(column) + 1
            worksheet = writer.sheets['Daily Task Log']
            if column_index == 7:
                column_width = column_width // 2
            worksheet.set_column(column_index, column_index, column_width)

        writer.save()

    def print_email(self):
        date, day, name = self.logs[0][:3]
        subject = f"{name}'s Daily Task Log for {day} {date}"
        send_email(subject)
