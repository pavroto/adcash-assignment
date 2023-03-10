from django.urls import path

from . import views

app_name = 'uiapp'
urlpatterns = [
    path('', views.index, name="index"),
    path('signin/', views.signin, name="signin"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_view, name="logout")
]
