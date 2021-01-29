from django.urls import path
from currency_exchange.views import BaseCurrenciesListView, RateExchangeView

urlpatterns = [
    path('list/', BaseCurrenciesListView.as_view()),
    path('rates/', RateExchangeView.as_view()),
]
