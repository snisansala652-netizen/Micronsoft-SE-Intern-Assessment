from django.test import TestCase, Client
from django.urls import reverse
from api.models import Product, Sale, Transaction
import json

class CheckoutTestCase(TestCase):
    def setUp(self):
        # Before starting the test, a temporary product is created in the database.
        self.product = Product.objects.create(
            id=1, 
            name="Test Mouse", 
            price=1000, 
            stock=5
        )
        self.client = Client()
        self.url = reverse('checkout')

    def test_successful_checkout(self):
        """Checking if an item can be successfully purchased"""
        payload = {
            "items": [{"id": 1}]
        }
        response = self.client.post(
            self.url, 
            data=json.dumps(payload), 
            content_type='application/json'
        )
        
        # The response is also 200 (Success).
        self.assertEqual(response.status_code, 200)
        
        # Checking if the stock has decreased from 5 to 4
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 4)
        
        # Checking whether sales and transaction records have been created
        self.assertEqual(Sale.objects.count(), 1)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_insufficient_stock(self):
        """Checking if checkout stops when out of stock is encountered"""
        # Setting the stock to 0
        self.product.stock = 0
        self.product.save()

        payload = {"items": [{"id": 1}]}
        response = self.client.post(
            self.url, 
            data=json.dumps(payload), 
            content_type='application/json'
        )

        # The response should be 400 (Bad Request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Insufficient stock", response.data['error'])