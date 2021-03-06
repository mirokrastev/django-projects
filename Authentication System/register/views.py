from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def register_form(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username, password = form.cleaned_data['username'], form.cleaned_data['password1']
            form = authenticate(request, username=username, password=password)
            login(request, form)
            return redirect(home_view)
    else:
        form = UserCreationForm()

    return render(request, 'register/register.html', {'form': form})


def login_form(request):
    error = None
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        form = authenticate(request, username=username, password=password)

        if form:
            login(request, form)
            return redirect(home_view)

        error = 'Incorrect username or password! Please try again!'
    form = AuthenticationForm()

    return render(request, 'register/login.html', {'form': form, 'error': error})


def logout_form(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html', {'error': 'You are not logged in!'})

    if request.method == 'POST':
        logout(request)
        return redirect(home_view)

    return render(request, 'home.html', {'error': 'Please use the Logout button'})


def home_view(request):
    return render(request, 'home.html')
