from django.shortcuts import render


def index(request):
    return render(request, 'uiapp/index.html')


def signin(request):
    return render(request, 'uiapp/signin.html')


def register(request):
    return render(request, 'uiapp/register.html')
