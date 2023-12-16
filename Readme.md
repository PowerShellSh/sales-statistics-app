# MyFruitShop ウェブアプリケーション

このリポジトリには、MyFruitShop ウェブアプリケーションのソースコードと構成が含まれています。このアプリケーションは Django を使用し、データベースとして MySQL を利用しています。

## プロジェクトの構造
├── django
│ ├── Dockerfile
│ └── code
│ ├── entryscript.sh
│ ├── myfruitshop
│ │ ├── init.py
│ │ ├── debug.log
│ │ ├── fake.py
│ │ ├── fruit
│ │ │ ├── init.py
│ │ │ ├── admin.py
│ │ │ ├── apps.py
│ │ │ ├── migrations
│ │ │ ├── models.py
│ │ │ ├── tests.py
│ │ │ ├── urls.py
│ │ │ └── views.py
│ │ ├── manage.py
│ │ ├── myfruitshop
│ │ │ ├── init.py
│ │ │ ├── asgi.py
│ │ │ ├── settings.py
│ │ │ ├── urls.py
│ │ │ └── wsgi.py
│ │ ├── sales
│ │ │ ├── admin.py
│ │ │ ├── apps.py
│ │ │ ├── forms.py
│ │ │ ├── migrations
│ │ │ ├── models.py
│ │ │ ├── urls.py
│ │ │ └── views.py
│ │ ├── static
│ │ │ └── images
│ │ │ └── background.jpg
│ │ ├── templates
│ │ │ ├── add_fruit.html
│ │ │ └── ...
│ │ ├── templatetags
│ │ │ └── custom_filters.py
│ │ └── tests
│ │ └── ...
│ └── requirements.txt
├── mysql
│ ├── Dockerfile
│ └── data
│ ├── #ib_16384_0.dblwr
│ └── ...
├── docker-compose.yml
└── Readme.md

## 必要なもの

アプリケーションを実行する前に、以下がインストールされていることを確認してください：

- Docker
- Docker Compose

## 始め方

1. このリポジトリをクローンします：

   ```bash
   git clone 
   cd myfruitshop

- Docker コンテナをビルドして実行します：

bash
docker-compose up --build

ウェブブラウザで http://localhost:80 にアクセスします。

# その他の情報
Django アプリケーションはポート 80 で実行されるように設定されています。
MySQL はポート 3306 で実行されるように設定されています。
詳細な設定については各 Dockerfile および docker-compose.yml を確認してください。
プロジェクトの詳細な説明や運用に関する情報は、プロジェクトの特定の要件に基づいて追加してください。
