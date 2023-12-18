from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from typing import Any, List, Union

from sales.models import Fruit, Sale
from sales.views import (
    FruitListView,
    AddFruitView,
    EditFruitView,
    DeleteFruitView,
    SaleCombinedView,
    AddSaleView,
    EditSaleView,
    DeleteSaleView,
    SalesAggregateView,
)

class FruitViewsTest(TestCase):
    def setUp(self) -> None:
        self.factory: RequestFactory = RequestFactory()
        self.user: User = User.objects.create_user(
            username='testuser',
            password='testpass',
        )

    @patch('sales.views.FruitListView.get_queryset')
    def test_fruit_list_view(self, mock_get_queryset: Any) -> None:
        mock_get_queryset.return_value = Fruit.objects.all()

        url: str = reverse('fruit')
        request: Any = self.factory.get(url)
        request.user = self.user

        response: Any = FruitListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @patch('sales.views.AddFruitView.get')
    def test_add_fruit_view(self, mock_get: Any) -> None:
        mock_get.return_value = None

        url: str = reverse('add_fruit')
        request: Any = self.factory.post(
            url, data={'name': 'Test Fruit', 'price': 10})
        request.user = self.user

        response: Any = AddFruitView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    @patch('sales.views.EditFruitView.get_object')
    def test_edit_fruit_view(self, mock_get_object: Any) -> None:
        fruit: Fruit = Fruit.objects.create(name='Apple', price=200)
        mock_get_object.return_value = fruit

        url: str = reverse('edit_fruit', kwargs={'pk': fruit.pk})
        request: Any = self.factory.get(url)
        request.user = self.user

        response: Any = EditFruitView.as_view()(request, pk=fruit.pk)
        self.assertEqual(response.status_code, 200)

    @patch('sales.views.DeleteFruitView.get_object')
    def test_delete_fruit_view(self, mock_get_object: Any) -> None:
        fruit: Fruit = Fruit.objects.create(name='Banana', price=100)
        mock_get_object.return_value = fruit

        url: str = reverse('delete_fruit', kwargs={'pk': fruit.pk})
        request: Any = self.factory.post(url)
        request.user = self.user

        response: Any = DeleteFruitView.as_view()(request, pk=fruit.pk)
        self.assertEqual(response.status_code, 302)


class SaleCombinedViewTest(TestCase):
    def setUp(self) -> None:
        self.factory: RequestFactory = RequestFactory()
        self.user: User = User.objects.create_user(
            username='testuser',
            password='testpass',
        )

    @patch('sales.views.Sale.objects.select_related')
    def test_sale_combined_view_get(self, mock_select_related: Any) -> None:
        mock_select_related.return_value.filter.return_value.order_by.return_value = Sale.objects.all()

        url: str = reverse('sales_combined')
        request: Any = self.factory.get(url)
        request.user = self.user

        response: Any = SaleCombinedView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class AddSaleViewTest(TestCase):
    def setUp(self) -> None:
        self.factory: RequestFactory = RequestFactory()
        self.user: User = User.objects.create_user(
            username='testuser',
            password='testpass',
        )

    @patch('sales.views.Fruit.objects.get')
    @patch('sales.views.Sale.objects.create')
    def test_add_sale_view_post(self, mock_create: Any, mock_get: Any) -> None:
        mock_get.return_value = Fruit.objects.create(
            name='Test Fruit', price=10)

        url: str = reverse('add_sales')
        request: Any = self.factory.post(
            url, data={'fruit': 'Test Fruit', 'quantity': 5}
        )
        request.user = self.user

        response: Any = AddSaleView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class EditSaleViewTest(TestCase):
    def setUp(self) -> None:
        self.factory: RequestFactory = RequestFactory()
        self.user: User = User.objects.create_user(
            username='testuser',
            password='testpass',
        )

    def test_edit_sale_view_post_without_mock(self) -> None:
        fruit: Fruit = Fruit.objects.create(name='Test Fruit', price=10)
        sale: Sale = Sale.objects.create(
            quantity=5, total_amount=50, sale_date='2023-01-01', fruit=fruit)

        url: str = reverse('edit_sales', kwargs={'pk': sale.pk})
        request: Any = self.factory.post(
            url, data={'fruit': 'Test Fruit', 'quantity': 10}
        )
        request.user = self.user

        response: Any = EditSaleView.as_view()(request, pk=sale.pk)

        expected_status_code: int = 200
        self.assertEqual(response.status_code, expected_status_code)


class DeleteSaleViewTest(TestCase):
    def setUp(self) -> None:
        self.factory: RequestFactory = RequestFactory()
        self.user: User = User.objects.create_user(
            username='testuser',
            password='testpass',
        )

    @patch('sales.views.DeleteSaleView.get_object')
    def test_delete_sale_view_post(self, mock_get_object: Any) -> None:
        sale: Sale = Sale.objects.create(fruit=Fruit.objects.create(
            name='Test Fruit', price=10), quantity=5, total_amount=50, sale_date='2023-01-01')
        mock_get_object.return_value = sale

        url: str = reverse('delete_sale', kwargs={'pk': sale.pk})
        request: Any = self.factory.post(url)
        request.user = self.user

        response: Any = DeleteSaleView.as_view()(request, pk=sale.pk)
        self.assertEqual(response.status_code, 302)


class SalesAggregateViewTest(TestCase):
    def setUp(self) -> None:
        self.factory: RequestFactory = RequestFactory()

    @patch('sales.views.Sale.objects.all')
    def test_sales_aggregate_view_get(self, mock_all: Any) -> None:
        mock_all.return_value = Sale.objects.all()

        url: str = reverse('sales_aggregate')
        request: Any = self.factory.get(url)

        response: Any = SalesAggregateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
