from datetime import time
from rest_framework.serializers import ModelSerializer, ValidationError
from currency_exchange.models import Rate
from django.utils import timezone
from requests import get

class RateExchangeSerializer(ModelSerializer):
    class Meta:
        model = Rate
        exclude = ['id', 'created_at']
        read_only_fields = ['date', 'rates']

    def call_exchange_api(self, base):
        rate = get(f"https://api.exchangeratesapi.io/latest?base={base}")
        if rate.status_code == 200:
            return rate.json()
        else:
            raise ValidationError(rate.json())

    def create(self, validated_data):
        base = validated_data['base']
        try:
            return Rate.objects.get(base=base, created_at=timezone.now().date())
        except:
            rates = self.call_exchange_api(base)
            instance = Rate.objects.create(**rates)
            return instance