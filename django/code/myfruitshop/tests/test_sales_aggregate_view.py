from django.test import TestCase
from datetime import datetime, timedelta, timezone
from sales.views import SalesAggregateView

class TestSalesAggregateView(TestCase):
    def override_current_time(self, new_time):
        datetime.now = lambda tz=None: new_time

    def test_init(self):
        # テスト用の現在時刻を設定
        current_time = datetime(2024, 1, 20, 12, 0, 0, 0, tzinfo=timezone.utc)

        # 現在時刻を一時的に書き換える
        with self.override_current_time(current_time):
            # インスタンスの作成
            view = SalesAggregateView()

        # end_of_dayのテスト
        expected_end_of_day = datetime(2024, 1, 20, 23, 59, 59, tzinfo=timezone(timedelta(hours=9)))
        self.assertEqual(view.end_of_day, expected_end_of_day)
        # start_date_monthlyのテスト
        expected_start_date_monthly = datetime(2023, 11, 1, 0, 0, 0, tzinfo=timezone(timedelta(hours=9)))
        self.assertEqual(view.start_date_monthly, expected_start_date_monthly)
        # start_date_dailyのテスト
        expected_start_date_daily = datetime(2024, 1, 18, 0, 0, 0, tzinfo=timezone(timedelta(hours=9)))
        self.assertEqual(view.start_date_daily, expected_start_date_daily)
