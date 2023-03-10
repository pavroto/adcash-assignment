from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, Http404
from .guard import input_test

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User


def index(request):
    if request.user.is_authenticated:
        return render(request, 'uiapp/index.html', {'question': request.user.get_username()})
    return render(request, 'uiapp/index.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('uiapp:index'))
    else:
        return HttpResponseRedirect(reverse('uiapp:index'))


def signin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('uiapp:index'))

    if request.method == 'POST':
        input_map = {
            "username": request.POST['username'],
            "psw": request.POST['psw']
        }

        test_output = input_test(input_map, case='LOGIN')

        if test_output[0] is not None:
            user = authenticate(request, username=test_output[0]['username'], password=test_output[0]['psw'])

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('uiapp:index'))
        elif test_output[1] is not None:
            return render(request, 'uiapp/signin.html', {"error_list": test_output[1]})

        return render(request, 'uiapp/signin.html', {"error_list": ["Invalid login"]})

    return render(request, 'uiapp/signin.html')


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('uiapp:index'))

    if request.method == 'POST':

        input_map = {
            "first_name": request.POST['first_name'],
            "second_name": request.POST['second_name'],
            "username": request.POST['username'],
            "psw": request.POST['psw'],
            "psw_rp": request.POST['psw_rp']  # psw_rp means password repeat
        }

        test_output = input_test(input_map, case='REGISTER')

        if test_output[0] is not None:

            try:
                user = User.objects.get(username=test_output[0]['username'])
                return render(request, 'uiapp/register.html',
                              {"error_list": ["User with this username already exists"]})

            except User.DoesNotExist:
                User.objects.create_user(username=test_output[0]['username'], email=None,
                                         password=test_output[0]['psw'], first_name=test_output[0]['first_name'],
                                         last_name=test_output[0]['second_name'])

                user = authenticate(request, username=test_output[0]['username'], password=test_output[0]['psw'])
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('uiapp:index'))
            return Http404()

        elif test_output[1]:
            return render(request, 'uiapp/register.html', {"error_list": test_output[1]})

        else:
            return Http404()

    return render(request, 'uiapp/register.html')
