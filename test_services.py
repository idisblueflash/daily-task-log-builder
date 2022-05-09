from datetime import timedelta, datetime
import pytest

from services import BaseDailyLogRow, DefaultDailyLogRow, LogReader, DefaultDailyLog


class TestDailyLogRow:
    ROW_DATA = '7:30 AI recommendation investigate on Kourosh'
    SUBLINE_ROW_DATA = '7:30, AI recommendation investigate on Kourosh: * foo * bar'
    STATUS_ROW_DATA = '7:30, AI recommendation investigate on Kourosh, Serge'
    DATE = '25/Apr/22'

    def get_service(self):
        service = DefaultDailyLogRow(self.ROW_DATA, self.DATE)
        service.parse()
        return service

    def test_parse_time(self):
        row = self.get_service()
        assert row.start_time == timedelta(hours=7, minutes=30)

    def test_parse_description(self):
        row = self.get_service()
        assert row.description == 'AI recommendation investigate on Kourosh'

    def test_parse_default_status(self):
        row = self.get_service()
        assert row.status == 'DONE'

    @pytest.mark.parametrize('test_input, expected', [
        ('AI recommendation investigate on Kourosh', 'Investigation'),
        ('DevOps Daily Meeting', 'Communication'),
        ('Discuss on Source collection', 'Discussion'),
        ('Email Status Test & communication', 'Communication'),
        ('Pairing on Other Source Setting up', 'Pairing'),
        ('New Feature on Center discussing', 'Discussion'),
        ('Compose daily Report', 'Daily Works'),
        ('take a break', 'Break'),
        ('not exist category', 'Tasks')

    ])
    def test_get_category(self, test_input, expected):
        result = BaseDailyLogRow._get_category(test_input)
        assert result == expected

    def test_get_date(self):
        row = self.get_service()
        assert row.date == '25/Apr/22'

    def test_get_day(self):
        row = self.get_service()
        assert row.day == 'Mon'

    def test_get_default_duration(self):
        row = self.get_service()
        assert row._get_duration() == 0

    def test_get_duration(self):
        row = self.get_service()
        row.end_time = timedelta(hours=10)
        assert row._get_duration() == 2.5

    def test_get_duration_with_round(self):
        row = self.get_service()
        row.end_time = timedelta(hours=8, minutes=19)
        assert row._get_duration() == 0.82

    def build_daily_log_row(self, *args):
        class StubDefaultDailyLogRow(DefaultDailyLogRow):
            person = 'Flash'

        return StubDefaultDailyLogRow(*args)

    def test_get_default_person(self):
        row = self.build_daily_log_row(self.ROW_DATA, '26/Apr/22')
        assert row._get_person('') == 'Flash'

    def test_get_default_time(self):
        row = self.get_service()
        assert row._get_time() == '7:30 - ?'

    def test_get_time(self):
        row = self.get_service()
        row.end_time = timedelta(hours=10)
        assert row._get_time() == '7:30 - 10:00'

    def test_get_person_with_one(self):
        row = self.build_daily_log_row(self.ROW_DATA, '26/Apr/22')
        assert row._get_person('Serge') == 'Flash, Serge'

    def test_get_person_with_one_and_space(self):
        row = self.build_daily_log_row(self.ROW_DATA, '26/Apr/22')
        assert row._get_person(' Serge') == 'Flash, Serge'

    def test_get_person_with_more(self):
        row = self.build_daily_log_row(self.ROW_DATA, '26/Apr/22')
        assert row._get_person('Serge Kimi') == 'Flash, Serge, Kimi'

    @pytest.mark.parametrize('test_input, expected', [
        ('AI recommendation investigate on Kourosh', 'High'),
        ('DevOps Daily Meeting', 'Medium'),
        ('Discuss on Source collection', 'Medium'),
        ('Email Status Test & communication', 'Medium'),
        ('Pairing on Other Source Setting up', 'Medium'),
        ('New Feature on Center discussing', 'Medium'),
        ('Compose daily Report', 'Low'),
        ('break', 'Low')

    ])
    def test_get_priority(self, test_input, expected):
        result = DefaultDailyLogRow(None, None)._get_priority(test_input)
        assert result == expected


class TestDailyLog:
    def get_service(self):
        data = ['7:30, AI recommendation investigate on Kourosh',
                '10:00, DevOps Daily Meeting, Serge',
                '12:00, break']
        return DefaultDailyLog('26/Apr/22', data)

    def test_set_end_time(self):
        service = self.get_service()
        service.handle()
        assert service.logs[0].end_time == timedelta(hours=10)

    def test_remove_break_category(self):
        service = self.get_service()
        service.handle()
        assert len(service.logs) == 2

    def test_report(self):
        service = self.get_service()
        service.handle()
        service.report()


class TestLogReader:
    def get_reader(self):
        class StubLogReader(LogReader):
            file_name = 'demo.md'

            def _get_lines(self):
                return [
                    '# 27/Apr/22\n',
                    '8:00, foo',
                    '8:30, bar',
                    '9:00, break'
                    '\n',
                    '# 26/Apr/22\n',
                    '8:00, daily warms up: * email * zulip * planning\n',
                    '8:30, #8280 AI Recommend by email is broken: * setup up debug tools\n',
                    '9:19, Wrong Ask Formatting Emails Issue: communicate with Helen\n',
                    '# 25/Apr/22\n',
                    '8:00, daily warms up',
                    '  * email',
                    '  * zulip',
                    '8:30, tasks'
                ]

        reader = StubLogReader(None)
        reader._parse_file()
        return reader

    def test_parse_title(self):
        reader = self.get_reader()
        assert list(reader.data.keys())[0] == '27/Apr/22'

    def test_parse_logs(self):
        reader = self.get_reader()
        assert list(reader.data.values())[0] == ['8:00, foo', '8:30, bar', '9:00, break']

    def test_parse_second_title(self):
        reader = self.get_reader()
        assert list(reader.data.keys())[1] == '26/Apr/22'

    def test_parse_second_logs(self):
        reader = self.get_reader()
        assert list(reader.data.values())[1] == ['8:00, daily warms up: * email * zulip * planning',
                                                 '8:30, #8280 AI Recommend by email is broken: * setup up debug tools',
                                                 '9:19, Wrong Ask Formatting Emails Issue: communicate with Helen']

    def test_parse_multiple_lines(self):
        reader = self.get_reader()
        assert list(reader.data.values())[2] == ['8:00, daily warms up\n  * email\n  * zulip',
                                                 '8:30, tasks']

    def test_stared_with_time(self):
        reader = self.get_reader()
        assert reader._has_started_with_time('8:00, task')

    def test_not_stared_with_time(self):
        reader = self.get_reader()
        assert not reader._has_started_with_time('  * task')
