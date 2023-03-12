from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    debt = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    term = models.DateField()

    def get_amount(self):
        return self.amount

    def get_debt(self):
        return self.debt

    def get_term(self):
        return self.term

    def get_full_name(self):
        return self.user.get_full_name()

    def get_username(self):
        return self.user.get_username()

    def get_timestamp(self):
        return self.timestamp


class BlackList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)