from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .guard import input_test


def index(request):
    return render(request, 'uiapp/index.html')


def signin(request):
    return render(request, 'uiapp/signin.html')


def register(request):
    if request.method == 'POST':
        input_map = {
            "first_name": request.POST['first_name'],
            "second_name": request.POST['second_name'],
            "username": request.POST['username'],
            "psw": request.POST['psw'],
            "psw_rp": request.POST['psw_rp']  # psw_rp means password repeat
        }

        test_output = input_test(input_map, if_signin=True)

        if test_output[1]:
            return render(request, 'uiapp/register.html', {"error_list": test_output[1]})
        else:
            return HttpResponseRedirect(reverse('uiapp:index'),)

    return render(request, 'uiapp/register.html')
