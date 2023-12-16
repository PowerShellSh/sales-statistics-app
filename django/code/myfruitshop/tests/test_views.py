from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch

from sales.models import Fruit
from sales.views import FruitListView, AddFruitView, EditFruitView, DeleteFruitView


class FruitViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
        )

    @patch('sales.views.FruitListView.get_queryset')
    def test_fruit_list_view(self, mock_get_queryset):
        # Mocking get_queryset to avoid database hits
        mock_get_queryset.return_value = Fruit.objects.all()

        url = reverse('fruit')
        request = self.factory.get(url)
        request.user = self.user

        response = FruitListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    @patch('sales.views.AddFruitView.get')
    def test_add_fruit_view(self, mock_get):
        # Mocking get to avoid actual view logic
        mock_get.return_value = None

        url = reverse('add_fruit')
        request = self.factory.post(
            url, data={'name': 'Test Fruit', 'price': 10})
        request.user = self.user

        response = AddFruitView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    @patch('sales.views.EditFruitView.get_object')
    def test_edit_fruit_view(self, mock_get_object):
        fruit = Fruit.objects.create(name='Apple', price=200)
        mock_get_object.return_value = fruit

        url = reverse('edit_fruit', kwargs={'pk': fruit.pk})
        request = self.factory.get(url)
        request.user = self.user

        response = EditFruitView.as_view()(request, pk=fruit.pk)
        self.assertEqual(response.status_code, 200)

    @patch('sales.views.DeleteFruitView.get_object')
    def test_delete_fruit_view(self, mock_get_object):
        fruit = Fruit.objects.create(name='Banana', price=100)
        mock_get_object.return_value = fruit

        url = reverse('delete_fruit', kwargs={'pk': fruit.pk})
        request = self.factory.post(url)
        request.user = self.user

        response = DeleteFruitView.as_view()(request, pk=fruit.pk)
        self.assertEqual(response.status_code, 302)
