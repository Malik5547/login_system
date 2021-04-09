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
            set_login_session(request)
            return render(request, 'login/success.html')
        else:
            return render(request, 'login/login.html', {'wrong_login': True})
    else:
        return render(request, 'login/login.html')


def is_login_valid(request):
    username_req = request.POST['username']
    password_req = request.POST['password']

    try:
        user = User.objects.filter(
            username=username_req,
            password=password_req,
        )
    except (KeyError, User.DoesNotExist):
        return False

    return True


def set_login_session(request):
    request.session['user'] = request.POST['username']