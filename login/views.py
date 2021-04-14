from django.shortcuts import render

from .models import User


def index(request):
    if is_logged(request):
        context = {'username': logged_user(request)}
        return render(request, 'login/index.html', context)
    else:
        return login(request)


def login(request):
    if not is_logged(request):
        if request.POST:
            if is_login_valid(request):
                login_session_set(request)
                return render(request, 'login/success.html')
            else:
                return render(request, 'login/login.html', {'wrong_login': True})
        else:
            return render(request, 'login/login.html')
    else:
        return index(request)


def logout(request):
    login_session_delete(request)
    return login(request)


def is_logged(request):
    user = request.session.get('username')
    if user is None:
        return False
    else:
        return True


def logged_user(request):
    return request.session.get('username')


def is_login_valid(request):
    username_req = request.POST['username']
    password_req = request.POST['password']

    try:
        user = User.objects.get(
            username=username_req,
            password=password_req,
        )
    except (KeyError, User.DoesNotExist):
        return False

    return True


def login_session_set(request):
    request.session['username'] = request.POST['username']


def login_session_delete(request):
    del(request.session['username'])