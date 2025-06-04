from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class ProductHomeTestCase(TestCase):

    def test_view(self):
        path = reverse('home')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Home')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductListViewTestCase(TestCase):
    fixtures = ['products_fixture.json', 'categories_fixture.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_test_(response)
        self.assertEqual(list(response.context_data['products']), list(self.products[:6]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'cat_id': 1})
        response = self.client.get(path)

        self._common_test_(response)
        self.assertEqual(
            list(response.context_data['products']),
            list(self.products.filter(category_id=category.id))
        )

    def _common_test_(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Products')
        self.assertTemplateUsed(response, 'products/products.html')

