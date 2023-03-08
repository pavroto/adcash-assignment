from django.urls import path

from . import views

app_name = 'uiapp'
urlpatterns = [
    path('', views.index, name="index"),
]