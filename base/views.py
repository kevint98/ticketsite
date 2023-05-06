from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib import messages
from .forms import NewUserForm


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            login(request, user)
            return redirect('home')
        except:
            messages.error(
                request, "Incorrect email address or password. Please try again.")

    context = {"page": page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            # use Django's built-in validation
            pass

    context = {"form": form}
    return render(request, 'base/login_register.html', context)


@login_required(login_url='/login')
def home(request):
    user = request.user.name.split(" ")[0]
    return render(request, 'base/index.html', {'user': user})
