from django.db import connection
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.views import APIView

from bank.mock_responses import *
from bank.models import SupportedBanks, BankConnections
from bank.serializers import BankConnectionSerializer, BankTransactionSerializer

class BanksView(APIView):
    http_method_names = [u'get']

    def get(self, request):
        banks = SupportedBanks.objects.all()
        bank_list = [
                {
                    "bank_id":bank.id,
                    "bank_name":bank.bank_name,
                    "branches":list(bank.branch.values('branch_number','id'))
                } 
                for bank in banks] 

        return Response(data=bank_list)

class BankConnectionView(ListCreateAPIView):
    serializer_class = BankConnectionSerializer

    def list(self, request, *args, **kwargs):
        """
        Return a list of connections status for each user's bank connection wheather it connected or not
        """
        queryset = BankConnections.objects.filter(user=self.request.user)
        
        response = [{
            "connected": True if connection.isTokenValid else False,
            "bank": connection.bank_branch.bank.id
        } for connection in queryset]

        return Response(response)          

    def create(self, request, *args, **kwargs):

        response_type = request.query_params.get("response_type", "success")

        serializer = self.get_serializer(data=request.data, context={"user":request.user})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response = connect_to_bank(instance, response_type=response_type)
        headers = self.get_success_headers(serializer.data)
        return Response(response, headers=headers)

class BankTransactionView(CreateAPIView):
    serializer_class = BankTransactionSerializer

    def create(self, request, *args, **kwargs):

        response_type = request.query_params.get("response_type", "success")
    
        serializer = self.get_serializer(data=request.data, context={"user":request.user})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response = upload_money(instance, response_type=response_type)
        headers = self.get_success_headers(serializer.data)
        return Response(response, headers=headers)