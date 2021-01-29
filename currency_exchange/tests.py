from django.http import response
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from currency_exchange.models import Rate
from django.contrib.auth import get_user_model
import json

class RateCurrencyExchangeTest(APITestCase):
    def setUp(self):
        self.rate_api = "/currency/rates/"
        self.user_1 = {
            "email":"test1@test.com",
            "username":"test1",
            "password":"test1"
        }
        self.client = APIClient()
        self.client.post("/api/register/", json.dumps(self.user_1), content_type='application/json')
        user_obj = get_user_model().objects.first()
        self.client.force_authenticate(user_obj)

    def test_save_request_in_database(self):
        currency_response = self.client.get(path=f"{self.rate_api}?base=USD")
        self.assertEqual(currency_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Rate.objects.count(), 1)
        currency_response = self.client.get(f"{self.rate_api}?base=EUR")
        self.assertEqual(Rate.objects.count(), 2)
        # same as the first one should not insert in database and retreive the existing one
        currency_response = self.client.get(f"{self.rate_api}?base=USD")
        self.assertEqual(Rate.objects.count(),2)

    def test_not_supported_currency(self):
        currency_response = self.client.get(f"{self.rate_api}?base=mmm")
        self.assertEqual(currency_response.status_code, status.HTTP_400_BAD_REQUEST)
