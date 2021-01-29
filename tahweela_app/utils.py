from django.apps import apps
from django.utils import timezone
from django.db.models import Sum

def update_users_balance(receiver_user, amount, sender_user=None):
    TahweelaAccount = apps.get_model("tahweela_app", "TahweelaAccount")
    receiver_user_account = TahweelaAccount.objects.get(user=receiver_user)
    receiver_user_account.tahweela_balance += amount
    receiver_user_account.save()

    if sender_user:
        sender_user_account = TahweelaAccount.objects.get(user=sender_user)
        sender_user_account.tahweela_balance -= amount
        sender_user_account.save()

def check_limit_exceeded(user_transactions,  amount):
    daily_sum = user_transactions.filter(transaction_date__date=timezone.now().date()).aggregate(total=Sum('amount'))['total'] or 0
    if daily_sum+ amount > 10000:
        return ({"status":f"cannot exceed daily limit 10000 with amount {amount} your daily sum is {daily_sum}"})

    weekly_sum = user_transactions.filter(transaction_date__date=timezone.now().date()-timezone.timedelta(days=7)).aggregate(total=Sum('amount'))['total'] or 0
    if weekly_sum+ amount > 50000:
        return {"status":f"cannot exceed weekly limit 50000 with amount {amount} your weekly sum is {weekly_sum}"}