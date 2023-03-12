from django.urls import path

from . import views

app_name = 'apiapp'
urlpatterns = [
    path('', views.list_loans, name="list_loans"),
]
