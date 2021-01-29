from django.db import models

from django.contrib.auth import get_user_model
from django.utils import timezone

class SupportedBanks(models.Model):
    bank_name = models.CharField(max_length=50)
    bank_api = models.CharField(max_length=100)
    token_lifetime_in_minutes = models.SmallIntegerField(default=20)

    def __str__(self):
        return self.bank_name

class BankBranches(models.Model):
    branch_number = models.CharField(max_length=50)
    bank = models.ForeignKey("bank.SupportedBanks", related_name="branch", on_delete=models.CASCADE)

    def __str__(self):
        return self.branch_number

class BankConnections(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="bank_connection", on_delete=models.CASCADE)
    bank_branch = models.ForeignKey("bank.BankBranches", related_name="bank_connection", on_delete=models.CASCADE)

    account_number = models.CharField(max_length=30)
    account_name = models.CharField(max_length=70)
    connected = models.BooleanField(default=False)
    valid_token = models.CharField(max_length=250, default='')

    established_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status

    @property
    def isTokenValid(self):
        if self.valid_token:
            if (self.updated_at + timezone.timedelta(minutes=self.bank_branch.bank.token_lifetime_in_minutes)) > timezone.now():
                return True
            else:
                self.valid_token = ""
                self.connected = False
                self.save()
        return False

class BankTransaction(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="bank_transaction", on_delete=models.CASCADE)
    bank = models.ForeignKey("bank.SupportedBanks", related_name="bank_transaction", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=100, default="pending")
    transaction_reference_number = models.CharField(max_length=50, default='')

    transaction_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)