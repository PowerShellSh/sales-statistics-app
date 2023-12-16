from decimal import Decimal
from django.utils import timezone
from django.utils.timezone import make_aware, make_naive
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, UpdateView, DeleteView, View
)
from django.shortcuts import redirect, render
from django.utils import timezone
from django.db import models
from .models import Fruit, Sale
from .forms import SaleCombinedForm, SaleAddForm, FruitForm, BulkSaleForm, SaleEditForm
from io import TextIOWrapper
import csv
import logging
from typing import List, Tuple, Dict, Any, Union
from datetime import datetime, timedelta
from collections import defaultdict
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
LOGIN_URL = '/login/'


class FruitListView(LoginRequiredMixin, ListView):
    model = Fruit
    template_name = 'fruit_list.html'
    context_object_name = 'fruits'
    ordering = ['-created_at']
    queryset = Fruit.objects.filter(is_active=True)


class DeleteFruitView(LoginRequiredMixin, DeleteView):
    login_url = LOGIN_URL
    model = Fruit
    success_url = reverse_lazy('fruit')
    template_name = 'fruit_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()

        return redirect(success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class EditFruitView(LoginRequiredMixin, UpdateView):
    login_url = LOGIN_URL
    model = Fruit
    template_name = 'edit_fruit.html'
    form_class = FruitForm
    success_url = reverse_lazy('fruit')
    http_method_names = ['get', 'post', ]

    def get_object(self, queryset=None):
        logger.info('This is an info message in get_object method.')
        return super().get_object(queryset)

    def form_valid(self, form):
        logger.info('This is an info message in form_valid method.')
        # フォームのバリデーションが成功した場合の処理
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fruit_id'] = self.kwargs['pk']
        return context


class AddFruitView(LoginRequiredMixin, View):
    login_url = LOGIN_URL
    template_name = 'add_fruit.html'

    def get(self, request):
        form = FruitForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FruitForm(request.POST)

        if form.is_valid():
            fruit_name = form.cleaned_data['name']
            existing_fruit = Fruit.objects.filter(name=fruit_name).first()

            if existing_fruit:
                # 既に同じ名前の果物が存在する場合
                existing_fruit.is_active = True
                existing_fruit.price = form.cleaned_data['price']
                existing_fruit.created_at = timezone.now()
                existing_fruit.updated_at = timezone.now()
                existing_fruit.save()
            else:
                # 同じ名前の果物が存在しない場合
                form.save()

            return redirect('fruit')

        return render(request, self.template_name, {'form': form})


class SaleCombinedView(LoginRequiredMixin, View):
    login_url = LOGIN_URL
    template_name = 'sales_list_combined.html'
    paginate_by = 10  # ページあたりのアイテム数

    def get(self, request):
        sales = Sale.objects.select_related('fruit').filter(
            is_active=True).order_by('-sale_date')

        paginator = Paginator(sales, self.paginate_by)
        page = request.GET.get('page')
        sales = paginator.get_page(page)

        form_sale = SaleCombinedForm()
        form_bulk_sale = BulkSaleForm()

        return render(request, self.template_name, {'sales': sales, 'form_sale': form_sale, 'form_bulk_sale': form_bulk_sale})

    def post(self, request, *args, **kwargs):
        form_bulk_sale = BulkSaleForm(request.POST, request.FILES)

        if form_bulk_sale.is_valid():
            csv_file = TextIOWrapper(
                request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.reader(csv_file)
            for row in reader:
                fruit_name, quantity, total_amount, sale_date = row

                try:
                    fruit = Fruit.objects.get(name=fruit_name)
                except Fruit.DoesNotExist:
                    continue

                current_price = fruit.price
                expected_total_amount = int(quantity) * current_price

                try:
                    # 日付の形式が正しくない場合はValidationErrorが発生
                    datetime.strptime(sale_date, "%Y-%m-%d %H:%M")
                except ValueError:
                    continue

                if int(total_amount) != expected_total_amount:
                    continue

                Sale.objects.create(
                    fruit=fruit,
                    quantity=int(quantity),
                    total_amount=int(total_amount),
                    sale_date=sale_date
                )

        return self.get(request, *args, **kwargs)


class AddSaleView(LoginRequiredMixin, View):
    login_url = LOGIN_URL
    template_name = 'add_sales.html'

    def get(self, request):
        form = SaleAddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form_sale = SaleAddForm(request.POST)

        if form_sale.is_valid():
            sale = form_sale.save(commit=False)
            fruit_name = form_sale.cleaned_data.get('fruit')
            quantity = form_sale.cleaned_data.get('quantity')

            # Fruitが存在するか確認
            try:
                fruit = Fruit.objects.get(name=fruit_name)
            except Fruit.DoesNotExist:
                form_sale.add_error('fruit', '選択した果物は存在しません。')
                return render(request, self.template_name, {'form': form_sale})

            # SaleCombinedViewでのバリデーション
            current_price = fruit.price
            total_amount = quantity * current_price

            # 計算結果をsaleオブジェクトのtotal_amountフィールドに代入
            sale.total_amount = Decimal(total_amount)

            sale.save()
            logger.info('This is an info message in get_object AddSaleView.')
            return redirect('sales_combined')  # 保存後、販売情報管理画面にリダイレクト

        return render(request, self.template_name, {'form': form_sale})


class EditSaleView(LoginRequiredMixin, View):
    login_url = LOGIN_URL
    template_name = 'edit_sales.html'

    def get(self, request, pk):
        sale = get_object_or_404(Sale, pk=pk)
        form = SaleEditForm(instance=sale)
        return render(request, self.template_name, {'form': form, 'sale_id': pk})

    def post(self, request, pk):
        sale = get_object_or_404(Sale, pk=pk)
        form = SaleEditForm(request.POST, instance=sale)

        if form.is_valid():
            sale = form.save(commit=False)
            fruit_name = form.cleaned_data.get('fruit')
            quantity = form.cleaned_data.get('quantity')
            try:
                fruit = Fruit.objects.get(name=fruit_name)
            except Fruit.DoesNotExist:
                form.add_error('fruit', '選択した果物は存在しません。')
                return render(request, self.template_name, {'form': form})

            current_price = fruit.price
            total_amount = quantity * current_price

            # 計算結果をsaleオブジェクトのtotal_amountフィールドに代入
            sale.total_amount = Decimal(total_amount)
            form.save()
            return redirect('sales_combined')

        return render(request, self.template_name, {'form': form, 'sale_id': pk})


class DeleteSaleView(LoginRequiredMixin, DeleteView):
    login_url = LOGIN_URL
    model = Sale
    success_url = reverse_lazy('sales_combined')
    template_name = 'sale_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()

        return redirect(success_url)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class SalesAggregateView(View):
    template_name = 'sales_aggregate.html'

    def format_data(self, sales_data: List[models.Model], is_monthly: bool = True) -> List[Tuple[Tuple[Any, ...], Dict[str, Union[int, List[Dict[str, Union[str, Decimal, int]]]]]]]:
        formatted_data = defaultdict(lambda: {'total': 0, 'details': {}})

        # 期間の開始日を計算
        start_date = timezone.now() - relativedelta(months=3) if is_monthly else timezone.now() - timedelta(days=3)

        for sale in sales_data:
            # 指定された期間内のデータのみ処理
            if start_date <= sale.sale_date <= timezone.now() and sale.is_active:
                key = (sale.sale_date.year, sale.sale_date.month) if is_monthly else (sale.sale_date.year, sale.sale_date.month, sale.sale_date.day)
                total_amount = sale.total_amount

                # 新しいデータを作成する場合
                if key not in formatted_data:
                    formatted_data[key] = {'total': 0, 'details': {}}

                details = formatted_data[key]['details'].get(sale.fruit.name)

                # すでに同じ果物のデータがある場合は合算する
                if details:
                    details['amount'] += total_amount
                    details['quantity'] += sale.quantity
                else:
                    details = {'fruit': sale.fruit.name, 'amount': total_amount, 'quantity': sale.quantity}

                formatted_data[key]['details'][sale.fruit.name] = details
                formatted_data[key]['total'] += total_amount

        # 期間の部分をソート
        sorted_data = sorted(formatted_data.items(), key=lambda x: x[0])

        # 一番古いデータを削除
        if sorted_data and len(sorted_data) > 3:
            oldest_data = sorted_data[0]
            del formatted_data[oldest_data[0]]

        return formatted_data.items()


    def get(self, request, *args, **kwargs):
        # Get all sales data
        all_sales = Sale.objects.all()

        # 累計
        total_sales = sum(sale.total_amount for sale in all_sales if sale.is_active)

        # 月別集計
        today = timezone.now()
        # タイムゾーンを考慮して期間を指定
        start_date = today - timedelta(days=90)
        start_date = start_date.replace(tzinfo=timezone.utc)

        # Filter sales data for the specified conditions
        monthly_sales_data = [
            sale for sale in all_sales if start_date <= sale.sale_date <= today and sale.is_active
        ]
        monthly_data = self.format_data(monthly_sales_data)
        sorted_monthly_data = sorted(monthly_data, key=lambda x: x[0], reverse=True)

        # 日別集計
        daily_sales_data = [
            sale for sale in all_sales if today - timedelta(days=3) <= sale.sale_date <= today and sale.is_active
        ]
        daily_data = self.format_data(daily_sales_data, is_monthly=False)
        sorted_daily_data = sorted(daily_data, key=lambda x: x[0], reverse=True)

        context = {
            'total_sales': total_sales,
            'monthly_data': sorted_monthly_data,
            'daily_data': sorted_daily_data,
        }

        return render(request, self.template_name, context)
