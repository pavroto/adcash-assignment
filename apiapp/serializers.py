from rest_framework import serializers
from uiapp.models import Loan


class ListLoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'user', 'amount', 'debt', 'timestamp', 'term']

