from django.db import models
from django.contrib.auth import get_user_model
from tahweela_app.utils import update_users_balance

class TahweelaAccount(models.Model):
    user = models.OneToOneField(get_user_model(), related_name="tahweela_account", on_delete=models.CASCADE)
    tahweela_balance = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TahweelaTransaction(models.Model):
    tahweela_from = models.ForeignKey(get_user_model(), related_name="tahweela_from", on_delete=models.CASCADE)
    tahweela_to = models.ForeignKey(get_user_model(), related_name="tahweela_to", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    
    transaction_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_users_balance(self.tahweela_to, self.amount, self.tahweela_from)
