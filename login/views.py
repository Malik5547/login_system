from django.shortcuts import render

from .models import User


def index(request):
    user = request.session.get('user')
    if user is None:
        return login(request)
    else:
        context = {'user': user}
        return render(request, 'login/index.html', context)


def login(request):
    if request.POST:
        if is_login_valid(request):
            login_session_set(request)
            return render(request, 'login/success.html')
        else:
            return render(request, 'login/login.html', {'wrong_login': True})
    else:
        return render(request, 'login/login.html')


def logout(request):
    login_session_delete(request)
    return login(request)


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
    request.session['user'] = request.POST['username']


def login_session_delete(request):
    del(request.session['user'])