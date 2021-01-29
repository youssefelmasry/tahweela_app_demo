from rest_framework import serializers
from tahweela_app.models import TahweelaAccount, TahweelaTransaction
from django.contrib.auth import get_user_model
from tahweela_app.utils import check_limit_exceeded

class TahweelaTransactionSerializer(serializers.ModelSerializer):
    tahweela_to = serializers.CharField(max_length=100)
    
    class Meta:
        model = TahweelaTransaction
        fields = ['amount', 'tahweela_to']

    def limit_validation(self):
        user_transaction = TahweelaTransaction.objects.filter(tahweela_from=self.user)
        error = check_limit_exceeded(user_transaction, self.amount)
        if error:
            raise serializers.ValidationError(error)

    def get_tahweela_to(self):
        receiver = get_user_model().objects.filter(email=self.validated_data['tahweela_to']).last() or \
                    get_user_model().objects.filter(username=self.validated_data['tahweela_to']).last()
        
        if receiver:
            if receiver == self.context['user']:
                raise serializers.ValidationError({"status":"Cannot Enter Your Email or Username"})
            return receiver
        else:
             raise serializers.ValidationError({"status":"Invalid User's email or username"})

    def check_user_balance(self):
        user_balance = TahweelaAccount.objects.get(user=self.user).tahweela_balance
        if user_balance < self.amount:
            raise serializers.ValidationError({"status":"Not enough balance"})
    
    def create(self, validated_data):
        self.user = self.context['user']
        self.amount = self.validated_data['amount']
        self.check_user_balance()
        self.limit_validation()
        instance = TahweelaTransaction.objects.create(tahweela_from=self.user, tahweela_to=self.get_tahweela_to(), amount=validated_data['amount'])
        return instance