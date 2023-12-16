from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import TopPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('top/', TopPageView.as_view(), name='top'),    # プロジェクトのホームページに関連する URL パターン
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('sales/', include('sales.urls')),  # sales アプリケーションの URL 設定を include
]
