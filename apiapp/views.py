from django.http import JsonResponse
from uiapp.models import Loan
from .serializers import ListLoansSerializer


# Create your views here.

def list_loans(request):
    loans = Loan.objects.all()
    serializer = ListLoansSerializer(loans, many=True)
    return JsonResponse({'loans': serializer.data})
