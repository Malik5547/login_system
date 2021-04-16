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
                return render(request, 'login/success.html', {'msg': 'You have successfully signed in.'})
            else:
                return render(request, 'login/login.html', {'wrong_login': True})
        else:
            return render(request, 'login/login.html')
    else:
        return index(request)


def register_page(request):
    if not is_logged(request):
        if request.POST:
            reg_username = request.POST['username']
            reg_password = request.POST['password']

            if not is_registered(reg_username):
                register_account(reg_username, reg_password)
                return render(request, 'login/success.html', {'msg': 'You have successfully signed up.'
                                                                     'Now you can login.'})
            else:
                return render(request, 'login/register.html', {'already_registered': True})
        else:
            return render(request, 'login/register.html')
    else:
        return render(request, 'login/index.html')


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
        User.objects.get(
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


def is_registered(reg_username):
    try:
        User.objects.get(
            username=reg_username
        )
    except (KeyError, User.DoesNotExist):
        return False

    return True


def register_account(reg_username, reg_password):
    account = User(username=reg_username, password=reg_password)
    account.save()
