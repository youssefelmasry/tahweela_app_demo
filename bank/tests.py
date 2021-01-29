from os import stat
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from bank.models import SupportedBanks, BankBranches
import json
from time import sleep

class BankConnectionAndTransactionTest(APITestCase):
    def setUp(self):
        self.bank_connection_api = "/bank/connect/"
        self.bank_transaction_api = "/bank/upload/money/"
        self.user_1 = {
            "email":"test1@test.com",
            "username":"test1",
            "password":"test1"
        }
        self.connection_request = {
                        "bank":2,
                        "bank_branch": 4,
                        "account_number":"103902390923",
                        "account_name":"ahmed mansour"
                    }

        self.transaction_request = {"bank":1, "amount":5000}
        self.client = APIClient()
        self.client.post("/api/register/", json.dumps(self.user_1), content_type='application/json')
        self.user_obj = get_user_model().objects.first()
        self.client.force_authenticate(self.user_obj)

        SupportedBanks.objects.bulk_create(
            [SupportedBanks(bank_name="Ahly", bank_api="api", token_lifetime_in_minutes=0.05),
            SupportedBanks(bank_name="CIB", bank_api="api", token_lifetime_in_minutes=0.05)])

        BankBranches.objects.bulk_create(
            [BankBranches(bank_id=1, branch_number="doki"),
            BankBranches(bank_id=1, branch_number="zamalek"),
            BankBranches(bank_id=1, branch_number="mohandseen"),
            BankBranches(bank_id=2, branch_number="doki"),
            BankBranches(bank_id=2, branch_number="agouza")])

    ### Bank connection

    def test_success_connection(self):
        res = self.client.post(self.bank_connection_api, self.connection_request)
        self.assertEqual(self.user_obj.bank_connection.last().connected, True)

    def test_invalid_bank_token(self):
        self.client.post(self.bank_connection_api, self.connection_request)
        # wait 4 seconds as we assumed the token lifetime is 3 secs in setup
        sleep(4)
        res = self.client.get(self.bank_connection_api)
        self.assertEqual(res.json()[0]['connected'], False)

    def test_invalid_account_number(self):
        # mock bank response with invalid account number by passing a query param with the desired response
        res = self.client.post(f"{self.bank_connection_api}?response_type=invalid", self.connection_request)
        self.assertEqual(res.json()['connected'], False)
        self.assertEqual(res.json()['status'], "Invalid Account Number")

    
    ### Bank Transaction

    def test_success_transacton(self):
        res = self.client.post(self.bank_transaction_api, self.transaction_request)
        self.assertEqual(res.json()['money_uploaded'], True)
        # check user's tahweela balance after upload money from bank to his account
        self.assertEqual(self.user_obj.tahweela_account.tahweela_balance, 5000)

    def test_not_enough_bank_balance(self):
        res = self.client.post(f"{self.bank_transaction_api}?response_type=not_enough", self.transaction_request)
        self.assertEqual(res.json()['money_uploaded'], False)
        self.assertEqual(res.json()['status'], "No enough balance in your account")

    def test_limit_transaction_amount(self):
        self.client.post(self.bank_transaction_api, self.transaction_request)
        self.client.post(self.bank_transaction_api, self.transaction_request)
        res = self.client.post(self.bank_transaction_api, self.transaction_request)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.json()['status'], "cannot exceed daily limit 10000 with amount 5000 your daily sum is 10000")
        
