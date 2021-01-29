from django.urls import path
from bank.views import BanksView, BankConnectionView, BankTransactionView

urlpatterns = [
    path('bankslist/', BanksView.as_view()),
    path("connect/", BankConnectionView.as_view()),
    path("upload/money/", BankTransactionView.as_view()),
]
