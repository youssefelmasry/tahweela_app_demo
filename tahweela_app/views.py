from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status

from tahweela_app.models import TahweelaAccount
from tahweela_app.serializers import TahweelaTransactionSerializer

class TahweelaBalanceView(APIView):
    http_method_names = [u'get']

    def get(self, request):
        return Response({"current_tahweela_balance":TahweelaAccount.objects.get(user=request.user).tahweela_balance})

class TahweelaTransactionView(CreateAPIView):
    serializer_class = TahweelaTransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"user":request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status":"Transfer Success"}, status=status.HTTP_201_CREATED, headers=headers)