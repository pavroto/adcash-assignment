from rest_framework import serializers
from uiapp.models import Loan


class ListLoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'user', 'amount', 'debt', 'timestamp', 'term']


class Errors(object):
    def __init__(self, errors):
        self.errors = errors


class ListErrorsSerializer(serializers.Serializer):
    errors = serializers.ListField(
        child=serializers.CharField()
    )

# class ListErrorsSerializer(serializers.Serializer):
#     items = ItemSerializer(many=True)
