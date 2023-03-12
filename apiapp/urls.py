from django.urls import path

from . import views

app_name = 'apiapp'
urlpatterns = [
    path('', views.ListLoansView.as_view(), name="ListLoansView"),
]
