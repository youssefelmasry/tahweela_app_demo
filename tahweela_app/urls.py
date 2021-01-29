from django.urls import path
from tahweela_app.views import TahweelaBalanceView, TahweelaTransactionView

urlpatterns = [
    path("get/balance/", TahweelaBalanceView.as_view()),
    path("transfer/money/", TahweelaTransactionView.as_view()),
]
