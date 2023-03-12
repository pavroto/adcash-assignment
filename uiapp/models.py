from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    debt = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    term = models.DateField()


class BlackList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)