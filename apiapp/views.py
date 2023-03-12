from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import reverse
from uiapp.models import Loan
from .serializers import ListLoansSerializer, ListErrorsSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ListErrorsSerializer, Errors

from uiapp.guard import input_test, monthly_interest_calculation
from datetime import datetime, timedelta


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


class ApplyLoansView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            input_map = {
                'first_name': request.POST['first_name'],
                'second_name': request.POST['second_name'],
                'amount': request.POST['amount'],
                'term': request.POST['term']
            }
        except:
            return JsonResponse({'status': 'Invalid Input'})

        test_output = input_test(input_map, case='APPLY', request=request)

        if test_output[0] is not None:

            debt = monthly_interest_calculation(amount=test_output[0]['amount'], months=test_output[0]['term'])
            term = datetime.now() + timedelta(days=30 * test_output[0]['term'])

            loan = Loan.objects.create(amount=test_output[0]['amount'],
                                       term=term,
                                       user=request.user,
                                       debt=debt)
            loan.save()

            return JsonResponse({'status': "Success"})

        elif test_output[1] is not None:
            # return JsonResponse({'error_list': test_output[1]})
            obj = Errors(test_output[1])
            serializer = ListErrorsSerializer(obj)
            return JsonResponse({'status': serializer.data})
        else:
            return JsonResponse({'status': 'Error'})
