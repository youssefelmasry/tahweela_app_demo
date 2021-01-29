from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
import json

class TahweelaTransactionTest(APITestCase):
    def setUp(self):
        self.transfer_money_api = "/tahweela/transfer/money/"
        self.account_balance_api = "/tahweela/get/balance/"
        user_1 = {
            "email":"test1@test.com",
            "username":"test1",
            "password":"test1"
        }
        user_2 = {
            "email":"test2@test.com",
            "username":"test2",
            "password":"test2"
        }
        self.client_1 = APIClient()
        self.client_1.post("/api/register/", json.dumps(user_1), content_type='application/json')
        self.user1_obj = get_user_model().objects.first()
        self.client_1.force_authenticate(self.user1_obj)

        self.client_2 = APIClient()
        self.client_2.post("/api/register/", json.dumps(user_2), content_type='application/json')
        self.user2_obj = get_user_model().objects.last()
        self.client_2.force_authenticate(self.user2_obj)

    def test_not_enough_balance(self):
        res = self.client_1.post(self.transfer_money_api, {"amount":500, "tahweela_to":"test2"})
        self.assertEqual(res.json(),{"status": "Not enough balance"})

    def test_valid_transfer(self):
        tahweela_account = self.user1_obj.tahweela_account
        tahweela_account.tahweela_balance = 20000
        tahweela_account.save()
        res = self.client_1.post(self.transfer_money_api, {"amount":9000, "tahweela_to":"test2"})
        self.assertEqual(res.json(),{"status":"Transfer Success"})
        self.assertEqual(self.user2_obj.tahweela_account.tahweela_balance, 9000)

    def test_limit_exceeded(self):
        tahweela_account = self.user1_obj.tahweela_account
        tahweela_account.tahweela_balance = 20000
        tahweela_account.save()
        self.client_1.post(self.transfer_money_api, {"amount":9000, "tahweela_to":"test2"})
        res = self.client_1.post(self.transfer_money_api, {"amount":1500, "tahweela_to":"test2"})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json(), {"status":"cannot exceed daily limit 10000 with amount 1500 your daily sum is 9000"})

