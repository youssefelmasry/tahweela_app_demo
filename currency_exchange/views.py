from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from currency_exchange.serializers import RateExchangeSerializer
from rest_framework.response import Response
from currency_exchange.models import BaseCurrencies

class BaseCurrenciesListView(APIView):
    def get(self, request):
        queryset = BaseCurrencies.objects.values_list('currency', flat=True)
        return Response({"currencies":queryset})

class RateExchangeView(ListAPIView):
    serializer_class = RateExchangeSerializer

    def list(self, request):

        base = request.query_params.get('base', None)

        serializer = self.get_serializer(data={"base":base})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
