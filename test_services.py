from datetime import timedelta, datetime
import pytest

from services import DailyLogRow, DailyLog


class TestDailyLogRow:
    ROW_DATA = '7:30, AI recommendation investigate on Kourosh'
    STATUS_ROW_DATA = '7:30, AI recommendation investigate on Kourosh, Serge'
    DATE = '25/Apr/22'

    def test_parse_time(self):
        row = DailyLogRow(self.ROW_DATA, self.DATE)
        row.parse()
        assert row.start_time == timedelta(hours=7, minutes=30)

    def test_parse_description(self):
        row = DailyLogRow(self.ROW_DATA, self.DATE)
        row.parse()
        assert row.description == 'AI recommendation investigate on Kourosh'

    def test_parse_default_status(self):
        row = DailyLogRow(self.ROW_DATA, self.DATE)
        row.parse()
        assert row.status == 'DONE'

    @pytest.mark.parametrize('test_input, expected', [
        ('AI recommendation investigate on Kourosh', 'Investigation'),
        ('DevOps Daily Meeting', 'Communication'),
        ('Discuss on Source collection', 'Discussion'),
        ('Email Status Test & communication', 'Communication'),
        ('Pairing on Other Source Setting up', 'Pairing'),
        ('New Feature on Center discussing', 'Discussion'),
        ('Compose daily Report', 'Daily Works')

    ])
    def test_get_category(self, test_input, expected):
        result = DailyLogRow._get_category(test_input)
        assert result == expected

    def test_get_date(self):
        row = DailyLogRow(self.ROW_DATA, self.DATE)
        row.parse()
        assert row.date == datetime(2022, 4, 25)

    def test_get_day(self):
        row = DailyLogRow(self.ROW_DATA, '26/Apr/22')
        row.parse()
        assert row.day == 'Tue'

    def test_get_default_duration(self):
        row = DailyLogRow(self.ROW_DATA, '26/Apr/22')
        row.parse()
        assert row._get_duration() == 0

    def test_get_duration(self):
        row = DailyLogRow(self.ROW_DATA, '26/Apr/22')
        row.parse()
        row.end_time = timedelta(hours=10)
        assert row._get_duration() == 2.5


class TestDailyLog:
    def get_service(self):
        data = ['7:30, AI recommendation investigate on Kourosh',
                '10:00, DevOps Daily Meeting, done']
        return DailyLog('24/Apr/22', data)

    def test_set_end_time(self):
        service = self.get_service()
        service.handle()
        assert service.logs[0].end_time == timedelta(hours=10)
