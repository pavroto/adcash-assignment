from django.contrib import admin
from .models import Loan, BlackList

# Register your models here.

admin.site.register(Loan)
admin.site.register(BlackList)
