import os
import django
from faker import Faker
import random

# プロジェクトの settings モジュールをインポート
from myfruitshop.settings import BASE_DIR
from sales.models import Fruit, Sale

import os
import django

# Djangoの設定を読み込む
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myfruitshop.settings')
django.setup()

fake = Faker()

# Fruit データの生成
for _ in range(100):  # 100個の果物を生成する例
    Fruit.objects.create(
        name=fake.word(),
        price=random.uniform(0.5, 5.0)
    )

# Sale データの生成（三ヶ月分のデータを生成する例）
start_date = fake.date_between(start_date='-3M', end_date='today')

for _ in range(1000):  # 1000個の販売データを生成する例
    fruit = Fruit.objects.order_by('?').first()  # ランダムに果物を選択
    sale_date = fake.date_time_between_dates(datetime_start=start_date, tzinfo=None)
    Sale.objects.create(
        fruit=fruit,
        quantity=random.randint(1, 20),
        total_amount=fruit.price * random.randint(1, 20),
        sale_date=sale_date
    )
