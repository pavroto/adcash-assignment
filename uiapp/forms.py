from django import forms
from uiapp.guard import NAME_MIN_LENGTH, NAME_MAX_LENGTH
from uiapp.guard import APPLY_MIN_AMOUNT, APPLY_MAX_AMOUNT
from uiapp.guard import APPLY_MIN_MONTHS, APPLY_MAX_MONTHS


# todo Apply form
class ApplyForm(forms.Form):
    first_name = forms.CharField(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH)
    second_name = forms.CharField(min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH)
    amount = forms.FloatField(min_value=APPLY_MIN_AMOUNT, max_value=APPLY_MAX_AMOUNT)
    term = forms.IntegerField(min_value=APPLY_MIN_MONTHS, max_value=APPLY_MAX_MONTHS)
    # term is calculated in full months
