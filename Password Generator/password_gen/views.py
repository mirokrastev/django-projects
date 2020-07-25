from django.shortcuts import render
from random import choice


def home_view(request, *args, **kwargs):
    content = {'pass_length': list(range(6, 33))}

    return render(request, 'index.html', content)


def password_view(request):
    pass_length = int(request.GET.get('length'))
    chars = [chr(num) for num in range(97, 123)]

    if pass_length < 6:
        pass_length = 6
    elif pass_length > 32:
        pass_length = 32

    if request.GET.get('uppercase'):
        chars.extend([chr(num) for num in range(65, 91)])

    if request.GET.get('numbers'):
        chars.extend(list(map(str, range(10))))

    if request.GET.get('special'):
        chars.extend([chr(num) for num in range(33, 48)])
        chars.extend([chr(num) for num in range(58, 65)])

    password = "".join([choice(chars) for _ in range(pass_length)])

    return render(request, 'password.html', {'pass': password})


def about_view(request):
    return render(request, 'about.html')
