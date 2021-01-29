from django.db import models
from rest_framework import serializers
from bank.models import BankConnections, BankTransaction
from tahweela_app.utils import check_limit_exceeded

class BankConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankConnections
        fields = ['bank_branch', 'account_number', 'account_name', 'connected']
        optional_fields = ['connected']

    def create(self, validated_data):
        user = self.context['user']
        instance = BankConnections.objects.update_or_create(user=user, bank_branch__bank=validated_data['bank_branch'].bank, defaults=validated_data)[0]
        return instance

class BankTransactionSerializer(serializers.ModelSerializer):

    def limit_validation(self):
        user_transactions = BankTransaction.objects.filter(user=self.context['user'])
        error = check_limit_exceeded(user_transactions, self.validated_data['amount'])
        if error:
            raise serializers.ValidationError(error)

    class Meta:
        model = BankTransaction
        fields = ['amount', 'bank', 'transaction_date', 'status']
        read_only_fields = ['transaction_date']
        optional_fields = ['transaction_date', 'status']

    def create(self, validated_data):
        self.limit_validation()
        user = self.context['user']
        instance = BankTransaction.objects.create(user=user, **validated_data)
        return instance