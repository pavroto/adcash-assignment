from django.http import JsonResponse
from uiapp.models import Loan
from .serializers import ListLoansSerializer
from django.contrib.auth.models import User

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


def list_loans(request):
    loans = Loan.objects.all()
    serializer = ListLoansSerializer(loans, many=True)
    return JsonResponse({'loans': serializer.data})


class ListLoansView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user:
            loans = Loan.objects.filter(user=request.user).all()
            serializer = ListLoansSerializer(loans, many=True)
            return JsonResponse({'loans': serializer.data})
